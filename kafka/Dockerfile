FROM python:2.7.12-alpine

ENV SYMBOL "AAPL"
ENV TOPIC "stock-analyzer"
ENV KAFKA_LOCATION "192.168.99.100:9092

ADD . /code
RUN pip install -r /code/requirements.txt
CMD python /code/gdata-producer.py ${SYMBOL} ${TOPIC} ${KAFKA_LOCATION}
