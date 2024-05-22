def sms():


    print("""
    
    SMS MIGRATION

# Log in to the management console and choose Service List > Migration > Server
Migration Service

#INSTALL the SMS Agent
Log in to the ECS in the CN-Hong Kong region and run the following
commands to download the SMS Agent package:

wget -t 3 -T 15 https://sms-agent-2-0.obs.ap-southeast-1.myhuaweicloud.com/SMS-Agent.tar.gz
yum install -y rsync 



Run the following commands to decompress the Agent package and install Agent:
tar -zxvf SMS-Agent.tar.gz
cd SMS-Agent
./startup.sh
    
    """)