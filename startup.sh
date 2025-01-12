docker network create song_analysis_data_pipeline-network

# trigger streaming in docker
docker compose -f Docker/kafka/docker-compose.yml up --build -d

# trigger streaming in docker
docker compose -f Docker/streaming/docker-compose.yml up --build -d
