from kafka import KafkaConsumer
from cassandra.cluster import Cluster

import argparse
import atexit
import logging
import json


# topic_name = 'stock-analyzer'
# kafka_broker = '192.168.99.100:9092'
# key_space = 'stock'
# data_table = 'stock'
# cassandra_broker = '192.168.99.100:9042'

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)


def save_data(msg, cassandra_session):
    # print(msg)
    # - msg is Kafka ConsumerRecord
    parsed = json.loads(msg)[0]
    symbol = parsed.get('StockSymbol')
    tradeprice = float(parsed.get('LastTradePrice'))
    tradetime = parsed.get('LastTradeDateTime')
    # print(parsed)
    logger.info('received data from Kafka %s', parsed )

    # - use CQL statement to insert data
    statement = "INSERT INTO %s (stock_symbol, trade_time, trade_price) VALUES ('%s', '%s', %f)" % (data_table, symbol, tradetime, tradeprice)

    cassandra_session.execute(statement)
    logger.info('Saved data to Cassandra, symbol: %s, tradetime: %s, tradeprice: %f' % (symbol, tradetime,tradeprice))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the Kafka topic')
    parser.add_argument('kafka_broker', help='the location of Kafka broker')
    parser.add_argument('key_space', help='the keyspace of cassandra')
    parser.add_argument('data_table', help='the table to use')
    parser.add_argument('cassandra_broker', help='the cassandra location')

    # - parse command line arguments
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    key_space = args.key_space
    data_table = args.data_table
    # - 192.168.99.100, 192....  an array
    cassandra_broker = args.cassandra_broker

    # - setup kafka consumer
    consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)

    # - setup cassandra session(client)
    cassandra_cluster = Cluster(contact_points=cassandra_broker.split(','))
    session = cassandra_cluster.connect(key_space)

    logger.info('connect to Kafka and Cassandra')

    for msg in consumer:
        logger.info(msg.value)
        save_data(msg.value, session)
