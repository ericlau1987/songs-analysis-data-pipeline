from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json
from pyspark.sql.types import *

from utils import prepare_dataframe_to_kafka_sink


class SongSparkStreaming:
    def __init__(self, 
        topic: str, 
        schema: str,
        spark_jars_packages: str, 
        spark_app_name: str = "song-streaming-data-pipeline", 
        kafka_bootstrap_servers: str = 'broker:29092', 
        starting_offsets: str = 'earliest', 
        fail_on_data_loss: bool = True,
        log_level: str = "INFO"
    ):
        self.spark_jars_packages = spark_jars_packages
        self.topic = topic
        self.schema = eval(schema)
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.starting_offsets = starting_offsets
        self.spark_app_name = spark_app_name
        self.log_level = log_level
        self.fail_on_data_loss = fail_on_data_loss
        self.spark = self._init_spark()

    def _init_spark(self):
        
        spark = SparkSession \
            .builder \
            .appName(self.spark_app_name) \
            .config("spark.jars.packages", self.spark_jars_packages) \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel(self.log_level)
        
        return spark
    
    def _transform_dataframe(self, df: DataFrame):
        
        df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        df = df.withColumn('json_value', from_json('value', self.schema)).select('key', 'value', 'json_value.*')
        
        return df
    
    def read(self):
        
        df_streaming_data = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.topic) \
            .option("startingOffsets", self.starting_offsets) \
            .option("failOnDataLoss", self.fail_on_data_loss) \
            .load()
            
        df_streaming_data = self._transform_dataframe(df_streaming_data)
            
        return df_streaming_data
    
    def write_to_kafka(self, 
            df: DataFrame, 
            topic: str, 
            output_mode: str = 'append', 
            kafka_checkpoint_location: str = 'checkpoint'
        ):
        
        df = prepare_dataframe_to_kafka_sink(df, key_column='key')
        
        kafka_writer = df.writeStream \
            .outputMode(output_mode) \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("topic", topic) \
            .option("checkpointLocation", kafka_checkpoint_location) \
            .start()
        
        return kafka_writer