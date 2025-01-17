from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_unixtime, hash, struct, to_json


def sink_console(df, output_mode: str = "complete", processing_time: str = "5 seconds"):
    write_query = (
        df.writeStream.outputMode(output_mode)
        .trigger(processingTime=processing_time)
        .format("console")
        .option("truncate", False)
        .start()
    )
    return write_query


def sink_memory(df, query_name, query_template):
    write_query = df.writeStream.queryName(query_name).format("memory").start()
    query_str = query_template.format(table_name=query_name)
    query_results = spark.sql(query_str)
    return write_query, query_results


def prepare_dataframe_to_kafka_sink(
    dataframe: DataFrame, key_column: str, value_columns: list = None
) -> DataFrame:
    if value_columns is None:
        value_columns = [c for c in dataframe.columns if c != key_column]

    dataframe = dataframe.withColumn("value", to_json(struct(*[value_columns])))
    return dataframe.select(["key", "value"])


def transform_epcho_to_timestamp(
    dataframe: DataFrame, timestamp_column: str
) -> DataFrame:
    dataframe = dataframe.withColumn("ts", col("ts") / 1000)
    dataframe = dataframe.withColumn(
        "ts", from_unixtime(col("ts"), "yyyy-MM-dd HH:mm:ss.SSSSSS")
    )

    return dataframe


def hash_key(dataframe: DataFrame, columns: list) -> DataFrame:
    dataframe = dataframe.withColumn("key", hash(*columns))
    return dataframe
