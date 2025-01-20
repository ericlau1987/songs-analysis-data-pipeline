FROM tabulario/spark-iceberg:3.5.0

COPY . /app

WORKDIR /app

# RUN pip install -r requirements.txt

# CMD ["spark-submit", "pyspark_consumer.py"]
