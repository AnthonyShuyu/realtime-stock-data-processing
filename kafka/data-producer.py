from googlefinance import getQuotes
from kafka import KafkaProducer

import argparse
import time
import json
import logging
import schedule
import atexit  # what will you do when you exit, shutdown_hook

# python has two import methods, import time: import the time package, and to
# use the package, need to use: time.time(). from kafka import KafkaProducer
# use the KafkaProducer, just use it directly

# kafka_broker = '192.168.99.100:9092'
# topic_name = 'stock-analyzer'

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)

# logger levels
    # - TRACE
    # - DEBUG
    # - INFO
    # - WARN
    # - ERROR

def fetch_price(producer, symbol):
    price = json.dumps(getQuotes(symbol))
    logger.debug('Get stock price %s', price)
    try:
        producer.send(topic=topic_name, value=price, timestamp_ms=time.time())
    except Exception:
        logger.warn('Failed to send message to Kafka')
    logger.debug('Successfully sent data to Kafka')
    # print(price)

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


"""
main fundation
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol', help='the stock symbol')
    parser.add_argument('topic_name', help='the kafka topic to push to')
    parser.add_argument('kafka_broker', help='location of kafka broker')

    args = parser.parse_args()
    symbol = args.symbol
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # - schedule and run every second
    schedule.every(1).second.do(fetch_price, producer, symbol)

    # - register shutdown hook
    atexit.register(shutdown_hook, producer)

    # - kick starter
    while True:
        schedule.run_pending()
        time.sleep(1)
