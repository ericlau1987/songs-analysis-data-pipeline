sbt assembly
chmod +x bin/eventsim

# output json files
# bin/eventsim --config examples/example-config.json --tag control -n 5000 \
#     --start-time "2015-06-01T00:00:00" --end-time "2015-09-01T00:00:00" \
#     --growth-rate 0.25 --userid 1 --randomseed 1 streaming_data/control.data.json

# output kafka brokers
bin/eventsim --config examples/example-config.json --tag control -n 5000 \
    --start-time "2015-06-01T00:00:00" --end-time "2015-07-01T00:00:00" \
    --growth-rate 0.25 --userid 1 --randomseed 1 --kafkaBrokerList broker:29092,broker:9092 streaming_data/control.data.json
