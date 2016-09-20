# Docker environment configuration script

## Script Code

local-setup.sh: quickly deploy single node Kakfa, Cassandra, Zookeeper, Redis development environment

## MacOS

1. create a docker-machine virturl machine, 2 CPUs, 2G memory
```sh
docker-machine create --driver virtualbox --virtualbox-cpu-count 2 --virtualbox-memory 2048 bigdata
```
2. run the script to start all the docker containers (Kafka, Cassandra, Zookeeper, Redis)
```sh
./local-setup.sh bigdata
```
