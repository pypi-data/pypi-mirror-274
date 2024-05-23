def diz():

    print("""
    
    DISCUZ INSTALLATION

# Download the web running environment.
	
	yum install -y httpd php php-fpm mysql php-mysql



#Start the web service and the environment and database services that the web
service depends on

	systemctl start httpd; systemctl enable httpd
	systemctl start php-fpm; systemctl enable php-fpm


# Install the website and download the website code. 

	wget https://hciecloud.obs.cn-north-4.myhuaweicloud.com/DiscuzENGUTF8.zip


# Decompress the website code package.
 	
	unzip DiscuzENGUTF8.zip 


# Save the website code to the root directory of the web service and modify the write
permission
	
	mv /root/DiscuzENGUTF8/* /var/www/html/
	chmod -R 777 /var/www/html 
    
    """)