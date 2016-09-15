# Docker环境配置相关脚本

## 脚本代码

local-setup.sh 快速部署单节点Kakfa, Cassandra, Zookeeper, Redis 开发环境

## MacOS

1. 创建一个docker-machine虚拟机, 2个CPU, 2G的内存
```sh
docker-machine create --driver virtualbox --virtualbox-cpu-count 2 --virtualbox-memory 2048 bigdata
```
2. 运行脚本来启动所有相关的docker容器 (Kafka, Cassandra, Zookeeper, Redis)
```sh
./local-setup.sh bigdata
```
