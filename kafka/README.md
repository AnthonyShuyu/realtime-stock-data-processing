# Kafka related codes

## data-producer.py

realize a Kafka producer, fetch a stock information per second from Google finance, and send to Kafka

### code dependences

googlefinance
https://pypi.python.org/pypi/googlefinance

kafka-python
https://github.com/dpkp/kafka-python

schedule
https://pypi.python.org/pypi/schedule

```sh
pip install -r requirements.txt
```

### run the code

if your Kafka runs on a docker-machine called bigdata, and the ip of the virtual machine is 192.168.99.100

```sh
python data-producer.py AAPL
stock-analyzer 192.168.99.100:9092
```


## fast-data-producer.py

realize another Kafka producer, produce random stock price and send to Kafka
Due to the large amount of data, be cautious to set the isolated development environment

### code dependences

confluent-kafka
https://github.com/confluentinc/confluent-kafka-python

### run the code

if your Kafka runs on a docker-machine called bigdata, and the ip of the virtual machine is 192.168.99.100

```sh
python fast-data-producer.py stock-analyzer 192.168.99.100:9092
```
