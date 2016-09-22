# - read from a kafka topic
# - publish data to redis PUB

from kafka import KafkaConsumer

import argparse
import atexit
import logging
import redis

# topic_name = ''
# kafka_broker = ''
# redis_channel = ''
# redis_host = ''
# redis_port = ''

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)



if __name__ == '__main__':
    # - setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the kafka topic to consumer from')
    parser.add_argument('kafka_broker', help='location of kafka broker')
    parser.add_argument('redis_channel', help='the redis channel to publish to') # the channel is the redis topic
    parser.add_argument('redis_host', help='the ip/url of redis_host, the location of the redis server')
    parser.add_argument('redis_port', help='the port of redis')

    # - parse arguments
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    redis_channel = args.redis_channel
    redis_host = args.redis_host
    redis_port = args.redis_port

    # - setup kafka consumer
    kafka_consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)

    # - setup redis client
    # - 9092(kafka), 9042(zookeeper), 6379(redis)
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

    for msg in kafka_consumer:
        logger.info('Received new data from kafka %s' % str(msg))
        redis_client.publish(redis_channel, msg.value)
