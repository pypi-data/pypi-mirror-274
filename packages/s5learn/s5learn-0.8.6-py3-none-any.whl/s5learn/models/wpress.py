def wpress():

    print("""
    
    #WORDPRESS INSTALLATION

#Install Linux, Apache, MySQL, PHP/Perl/Python (LAMP) and start related services
yum install -y httpd php php-fpm php-server php-mysql mysql 


# Download the WordPress installation package
wget -c https://cloudservice-v3.obs.cn-east3.myhuaweicloud.com/wordpress-4.9.10_en.tar.gz 


# Decompress the WordPress installation package to /var/www/html
tar -zxvf wordpress-4.9.10_en.tar.gz -C /var/www/html/ 

# Create a wp-config.php file. 
cd /var/www/html/wordpress 
 cp wp-config-sample.php wp-config.php 

# Configure database parameters in the wp-config.php file to interconnect with the
wordpress database. 
vi wp-config.php

# Grant read and write permissions to the directory where the package is
decompressed.

chmod -R 777 /var/www/html 

#Enable httpd and php-fpm
systemctl start httpd.service
systemctl start php-fpm.service

#Check the httpd service status. The status active (running) indicates that the httpd
service has been enabled. 
systemctl status httpd
systemctl status php-fpm 

# Set httpd and php-fpm to automatically start upon system startup.
systemctl enable httpd
systemctl enable php-fpm


#Run the following commands to configure permissions for the WordPress directory: 
cd /var/www/html/wordpress 

echo -e "define(\"FS_METHOD\", \"direct\");\ndefine(\"FS_CHMOD_DIR\", 0777) \ndefine(\"FS_CHMOD_FILE\", 0777);" >> wpconfig.php

tail -n 10 wp-config.php 
chmod -R 777 wp-content/ 



OPTIONAL


# Add the following information to the file to interconnect with the DCS instance:
cd /var/www/html/wordpress/
vi wp-config.php 
 
/*redis config*/
define('WP_REDIS_HOST', '192.168.2.IP');
define('WP_REDIS_PORT', '6379');
define('WP_REDIS_PASSWORD', 'DCS PASSWORD'); 
    
    """)