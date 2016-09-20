# Cassandra related codes

## data-storage.py
implement a process of data storage using Cassandra

### data dependences
cassandra-driver
https://github.com/datastax/python-driver

cql

```
pip install -r requirements.txt
```

### run the code

if your Cassandra runs on a docker-machine called bigdata, and the ip of the virtual machine is 192.168.99.100

use cqlsh client to create a keyspace(database) and a table

```
CREATE KEYSPACE "stock" WITH replication = {'class', 'SimpleStrategy', 'replication_factor': 1} AND durable_writes = 'true'l;
USE stock;
CREATE TABLE stock (stock_symbol text, trade_time timestamp, trade_price float, PRIMARY KEY(stock_symbol, trade_time))
```

```
python data-storage.py stock-analyzer
192.168.99.100:9092 stock stock 192.168.99.100
```
