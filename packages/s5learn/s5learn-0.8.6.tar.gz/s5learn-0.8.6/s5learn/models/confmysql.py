def confmysql():

    print("""
    
    INSTALL AND CONFIGURE MYSQL

rpm -Uvh https://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
yum -y install MySQL-community-server --nogpgcheck
systemctl start mysqld; systemctl enable mysqld


mysqldump -h   -P 3306 -u root -p --skip-lock-tables --add-locks=false --no-data magento > magento.sql    // Export the database table data file from rds

mysqldump -h   -P 3306 -u root -p --skip-lock-tables --add-locks=false --no-data magento > magento_data.sql    // Export the database table data file from rds

ls -l //view the result

MySQL -h ${}  - -P${} -u${} -p {}
    
    """)