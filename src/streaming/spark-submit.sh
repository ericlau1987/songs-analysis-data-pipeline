# Submit Python code to SparkMaster

if [ $# -lt 1 ]
then
	echo "Usage: $0 <pyspark-job.py> [ executor-memory ]"
	echo "(specify memory in string format such as \"512M\" or \"2G\")"
	exit 1
fi
PYTHON_JOB=$1

if [ -z $2 ]
then
	EXEC_MEM="1G"
else
	EXEC_MEM=$2
fi

TOPIC=$3

#TODO understand whether need to use --packages in the spark python script
spark-submit --master spark://spark-master:7077 --num-executors 4 \
	         --executor-memory 2G --executor-cores 4 \
             --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.apache.spark:spark-avro_2.12:3.3.1,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.1 \
             $PYTHON_JOB --topic $TOPIC
