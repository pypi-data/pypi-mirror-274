def impddm():


    print("""
    
    IMPORT DATA TO THE DDM SCHEMA

# Export the database table structure file from rds-hcie(rds-backup). Change the
following IP addresses to the database IP addresses. 



SAMPLE
	# TABLE STRUCTURE FILE
	mysqldump -h 0.0.0.0 -P 3306 -u root -p --skip-lock-tables --add-locks=false --no-data ultrax > ultrax.sql 

	#TABLE DATA FILE
	mysqldump -h 0.0.0.0 -P 3306 -u root -p --hex-blob --complete-insert --skip-lock-tables --skip-tz-utc --skip-add-locks --no-create-info ultrax > ultrax_data.sql



# Import the table structure to the DDM instance. (Change the IP address to that of
the purchased DDM instance.) 

SAMPLE
	mysql -f -h 0.0.0.0 -P 5066 -u root -p db_web < ultrax.sql

	mysql -f -h 0.0.0.0 -P 5066 -u root -p db_web < ultrax_data.sql 


    
    """)