# Node.js related code

## index.js

implement a simple Front-End application to display realtime dynamic data

### code dependences

socket.io
http://socket.io/

redis
https://www.npmjs.com/package/redis

smoothie        https://www.npmjs.com/package/smoothie

minimist        https://www.npmjs.com/package/minimist

```
npm install
```

### run the code

if your Kafka runs on a docker-machine called bigdata, and the ip of the virtual machine is 192.168.99.100

```
node index.js --port=3000 --redis_host=192.168.99.100 --redis_port=6379 --subscribe_topic=average-stock-price
```
