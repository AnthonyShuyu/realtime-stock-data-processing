# Spark related codes

## stream-process.py

### code dependences
pyspark         http://spark.apache.org/docs/latest/api/python/

kafka-python
https://github.com/dpkp/kafka-python

### run the code

if your Kafka runs on a docker-machine called bigdata, and the ip of the virtual machine is 192.168.99.100
```
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar stream-processing.py stock-analyzer average-stock-price 192.168.99.100:9092

```
