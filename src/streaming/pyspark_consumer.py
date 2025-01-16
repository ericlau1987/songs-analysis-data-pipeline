from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, LongType, IntegerType, StringType, FloatType, BooleanType
from pyspark.sql.functions import from_json

import yaml
import json
import os
from utils import *

with open('streaming_config.yml', 'r') as file:
    config = yaml.safe_load(file)

BOOTSTRAP_SERVERS = config['kafka']['bootstrap_servers']
STARTING_OFFSETS = config['kafka']['starting_offsets']
TOPIC = 'auth_events'
SCHEMA = config['kafka']['topics'][TOPIC]['schema']
SPARK_JARS_PACKAGES = config['spark']['spark_jars_packages']
STREAMING_KEY_COLUMNS = config['kafka']['topics'][TOPIC]['key_columns']
os.environ['PYSPARK_SUBMIT_ARGS'] = f'--packages {SPARK_JARS_PACKAGES}'

#TODO: rename the app name to remove topic name
#TODO: add multiple streaming queries together and be aware that only spark.streams.awaitAnyTermination() should be called once at the end.
spark = SparkSession \
    .builder \
    .appName(f"song-streaming-data-pipeline-{TOPIC}") \
    .config("spark.jars.packages", SPARK_JARS_PACKAGES) \
    .getOrCreate()
    
spark.sparkContext.setLogLevel("INFO")

df_kafka_raw = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
    .option("subscribe", TOPIC) \
    .option("startingOffsets", STARTING_OFFSETS) \
    .option("maxOffsetsPerTrigger", 2000) \
    .load()

df_kafka_encoded = df_kafka_raw.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
df_kafka_encoded = df_kafka_encoded.withColumn('json_value', from_json('value', eval(SCHEMA))).select('key', 'value', 'json_value.*')
df_kafka_encoded = transform_epcho_to_timestamp(df_kafka_encoded, 'ts')
df_kafka_encoded = hash_key(df_kafka_encoded, STREAMING_KEY_COLUMNS)
df_kafka_encoded = df_kafka_encoded.drop('value')
df_kafka_encoded = df_kafka_encoded.withColumn('key', df_kafka_encoded.key.cast(StringType()))
#TODO: add a function to convert spark schema to a list of columns
df_sink_kafka = prepare_dataframe_to_kafka_sink(df_kafka_encoded, key_columns=['key'], value_columns=['ts', 'sessionId', 'level', 'itemInSession', 'city', 'zip', 'state', 'userAgent', 'lon', 'lat', 'userId', 'lastName', 'firstName', 'gender', 'registration', 'tag', 'success'])
write_query = sink_kafka(df_sink_kafka, output_mode='append', topic=f'{TOPIC}_transformed')

spark.streams.awaitAnyTermination()