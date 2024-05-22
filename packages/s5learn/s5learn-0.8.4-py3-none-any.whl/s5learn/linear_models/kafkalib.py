def kafkalib():


    print("""
    
##login to kafa
cd /opt/client/Kafka/kafka/bin

##create a kafka topic
sh kafka-topics.sh --create --topic cx_topic2 --partitions 1 --replication-factor 1 --zookeeper 192.168.0.172:2181/kafka

##view topics 
sh kafka-topics.sh --list --zookeeper 192.168.0.172:2181/kafka

##create console consumer 
sh kafka-console-consumer.sh --topic cx_topic2 --bootstrap-server 192.168.0.119:9092 --consumer.config /opt/client/Kafka/kafka/config/consumer.properties

##create console producer 
sh kafka-console-producer.sh --broker-list 192.168.0.119:9092 --topic cx_topic2 --producer.config /opt/client/Kafka/kafka/config/producer.properties

##to list topics 
sh kafka-topics.sh --list --zookeeper 192.168.0.172:2181/kafka

##to delete a topic
sh kafka-topics.sh --delete --topic Topic name --IP address of the node where the ZooKeeper instance resides:clientPort/kafka

    """)