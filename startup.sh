docker network create song_analysis_data_pipeline-network

# trigger kafka in docker
docker compose -f Docker/kafka/docker-compose.yml up --build -d

# trigger streaming in docker
docker compose -f Docker/streaming/docker-compose.yml up --build -d

# trigger pyspark in docker
cd Docker/spark
sh build.sh
docker compose -f Docker/spark/docker-compose.yml up --build -d
