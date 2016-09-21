# - read from Kafka
# - do average
# - save data back

# import argparse (replaced by import sys, get the args from command line)
# compared to sys, the argparse may provide the function of help tips, which will remind you if you input the command wrong
import sys
import logging
import time
import json
from kafka import KafkaProducer
import atexit  # what will you do when you exit, shutdown_hook


# Context is the mechanic you can communicate with Spark

# from kafka.errors import KafkaError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
# you can choose where you get the straming data from, such as from pyspark.streaming.flume
from pyspark.streaming.kafka import KafkaUtils


logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)

# new_topic =

def process(timeobj, rdd):
    # do something after get the data
    # do average
    num_of_records = rdd.count()
    if num_of_records == 0:
        return

    # sum up all the prices in this rdd
    # for each rdd record, do something (take out the LastTradePrice, json) ->  map
    # for all the rdd record, sum up -> reduce

    # not best coding style, not good for coding review
    # you can use json_data = record[0] to pre check
    # lambda: anonymous function
    price_sum = rdd.map(lambda record: float(json.loads(record[1].decode('utf-8'))[0].get('LastTradePrice'))).reduce(lambda a, b: a + b)
    average = price_sum / num_of_records
    logger.info('Received records from Kafka, average price is %f:' % average)
    # print(price_sum)
    # print(num_of_records)
    current_time = time.time()
    data = json.dumps({'timestamp' : current_time, 'average': average})
    try:
        Kafka_producer.send(new_topic, value=data)
    except Exception:
        logger.warn('Failed to send message to Kafka new!')




"""
thi is a shutdown_hook, when your program has something related to IO, you need use the shutdown_hook
"""
def shutdown_hook(producer):
    logger.info('preparing to shutdown, waiting for producer to flush message')
    producer.flush(10)
    # guarantee you send your current data and not let other data come in
    # wait 10 seconds
    logger.info('producer flush finished')
    try:
        producer.close()
    except Exception:
        logger.warn('Failed to close producer')
    logger.info('producer closed')


if __name__ == '__main__':
    # arguments = sys.argv    this is an array
    # sys.argv[0] stream-process.py
    # sys.argv[1] broker location
    # sys.argv[2] topic
    # print(arguments)
    if (len(sys.argv) != 4):
        print("Not enough argument [Kafka broker location], [Kafka topic location], [Kafka new topic location]")
        exit(1)
    # where you run Spark, and the Spark app name
    sc = SparkContext('local[2]', 'StockAveragePrice')

    # -DEBUG, INFO, WARNING, ERROR(highest level)
    sc.setLogLevel('ERROR')
    # spark context, time period(within 5 seconds to do process(this is how to separate data))
    ssc = StreamingContext(sc, 5)

    kafka_broker, kafka_topic, new_topic = sys.argv[1:]

    # - setup a kafka stream
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [kafka_topic], {'metadata.broker.list': kafka_broker})
    directKafkaStream.foreachRDD(process)


    Kafka_producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # shutdown_hook
    # - register shutdown hook
    atexit.register(shutdown_hook, Kafka_producer)

    ssc.start()
    ssc.awaitTermination()
