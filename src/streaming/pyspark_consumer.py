import argparse
import json
import os

import yaml
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import (
    BooleanType,
    FloatType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)
from SongSparkStreaming import SongSparkStreaming
from utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Consumer")
    parser.add_argument("--topic", type=str)
    args = parser.parse_args()
    TOPIC = args.topic
    print(TOPIC)

    with open("streaming_config.yml", "r") as file:
        config = yaml.safe_load(file)

    BOOTSTRAP_SERVERS = config["kafka"]["bootstrap_servers"]
    STARTING_OFFSETS = config["kafka"]["starting_offsets"]
    # print(config['topics'])
    SCHEMA = config["topics"][TOPIC]["schema"]
    SPARK_JARS_PACKAGES = config["spark"]["spark_jars_packages"]
    STREAMING_KEY_COLUMNS = config["topics"][TOPIC]["key_columns"]

    os.environ["PYSPARK_SUBMIT_ARGS"] = f"--packages {SPARK_JARS_PACKAGES}"

    song_spark_streaming = SongSparkStreaming(
        topic=TOPIC,
        schema=SCHEMA,
        spark_app_name="song-analysis-pipeline",
        spark_jars_packages=SPARK_JARS_PACKAGES,
        kafka_bootstrap_servers=BOOTSTRAP_SERVERS,
        starting_offsets=STARTING_OFFSETS,
        fail_on_data_loss=False,
    )

    df = song_spark_streaming.read()

    df = transform_epcho_to_timestamp(df, "ts")
    df = hash_key(df, STREAMING_KEY_COLUMNS)
    df = df.drop("value")
    df = df.withColumn("key", df.key.cast(StringType()))

    kafka_writer = song_spark_streaming.write_to_kafka(df, topic=f"{TOPIC}_transformed")

    song_spark_streaming.spark.streams.awaitAnyTermination()
