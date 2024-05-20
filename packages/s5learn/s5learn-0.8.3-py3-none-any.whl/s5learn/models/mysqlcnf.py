def mysqlcnf():


    print("""
    
    MYSQL INSTALLATION ON ECS

# Run the following commands to install the MySQL database: 
cd /opt
wget https://hciecloud.obs.cn-north-4.myhuaweicloud.com/MySQL-5.6.45-1.el6.x86_64.rpm-bundle.tar
mkdir mysql_install
tar -xvf MySQL-5.6.45-1.el6.x86_64.rpm-bundle.tar -C mysql_install
cd mysql_install
yum -y remove mariadb*
yum install -y MySQL-shared-compat-5.6.45-1.el6.x86_64.rpm

#Modify the MySQL configuration file.
#Run the following command to add the my.cnf configuration file:

cat << EOF >> /etc/my.cnf
[mysqld]
join_buffer_size = 128M
sort_buffer_size = 2M
read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
# Disabling symbolic-links is recommended to prevent assorted security risks
lower_case_table_names = 1
innodb_strict_mode = 1
sql_mode =
symbolic-links=0
character_set_server = utf8
log-bin = mysql-bin
binlog_format=row
server-id = 2
expire_logs_days = 10
slave_skip_errors = 1062
innodb_strict_mode = 0

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
EOF

#Run the following command to start MySQL on the ecs-mysql ECS:
systemctl start MySQL


# Change the MySQL password on the  ECS. 

- Edit the mysql_pass.sh script.

#!/bin/bash
# Install the expect plug-in.
yum install -y expect
# Change the password to Huawei@123!.
pass=`awk -F"[ :]+" 'NR==1{print $NF}' /root/.mysql_secret`
/bin/expect << EOF
spawn /usr/bin/mysql -h127.0.0.1 -uroot -p`echo -e $pass`
expect "mysql>"
send "SET PASSWORD FOR root@localhost=PASSWORD('Huawei@123!');"
send "\n"
expect "mysql>"
send 'flush privileges\n'
expect "mysql>"
send 'quit\n'
interact
EOF

- Add the execute permission and run the script.
chmod +x mysql_pass.sh
./mysql_pass.sh

- Use the new password to log in to the MySQL database.
mysql -u root -pHuawei@123!



# Set database access permissions.
On the mysql> page, run the following command to grant the replication permission to
user root: 

grant all privileges on *.* to root@"%" identified by "Huawei@123!";
flush privileges; 
    
    """)