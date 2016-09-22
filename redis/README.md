# Redis related codes

## redis-publisher.py

Redis publisher(producer), receive messages from Kafka topic and publish to Redis PUB

### code dependences

kafka-python
https://github.com/dpkp/kafka-python

redis
https://pypi.python.org/pypi/redis

```
pip install -r requirements.txt
```

### run the code

if your Kafka runs on a docker-machine called bigdata, and the ip of the virtual machine is 192.168.99.100

```
python redis-publisher.py
average-stock-price 192.168.99.100:9092
average-stock-price 192.168.99.100:6379

```
