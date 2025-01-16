from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_unixtime, to_json, struct, hash

def sink_console(df, output_mode: str = 'complete', processing_time: str = '5 seconds'):
    write_query = df.writeStream \
        .outputMode(output_mode) \
        .trigger(processingTime=processing_time) \
        .format("console") \
        .option("truncate", False) \
        .start()
    return write_query 

def sink_memory(df, query_name, query_template):
    write_query = df \
        .writeStream \
        .queryName(query_name) \
        .format('memory') \
        .start()
    query_str = query_template.format(table_name=query_name)
    query_results = spark.sql(query_str)
    return write_query, query_results

def prepare_dataframe_to_kafka_sink(dataframe: DataFrame, key_columns: list, value_columns: list) -> DataFrame:
    
    dataframe = dataframe.withColumn("value", to_json(struct(*[c for c in dataframe.columns if c != 'key'])))
    return dataframe.select(['key', "value"])

def sink_kafka(dataframe: DataFrame, topic: str, output_mode: str = 'append', kafka_bootstrap_servers: str = 'broker:29092', kafka_checkpoint_location: str = 'checkpoint'):
    write_query = dataframe.writeStream \
        .outputMode(output_mode) \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("topic", topic) \
        .option("checkpointLocation", kafka_checkpoint_location) \
        .start()
    return write_query


def transform_epcho_to_timestamp(dataframe: DataFrame, timestamp_column: str) -> DataFrame:
    
    dataframe = dataframe.withColumn('ts', col('ts')/1000)
    dataframe = dataframe.withColumn('ts', from_unixtime(col('ts'), 'yyyy-MM-dd HH:mm:ss.SSSSSS'))
    
    return dataframe

def hash_key(dataframe: DataFrame, columns: list) -> DataFrame:
    dataframe = dataframe.withColumn('key', hash(*columns))
    return dataframe