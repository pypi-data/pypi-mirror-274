def ha10lib():


    print("""
    
sqoop command to connect to the MySQL database and list the database names. Replace xxx in the command with the password of MySQL database user root.
sqoop list-databases --connect jdbc:mysql://116.63.197.140:3306/ --username root --password xxx

sqoop command to import the data table from the MySQL database to the Hive table:
sqoop import --connect jdbc:mysql://116.63.197.140:3306/rdsdb --username root --password xxx --table cx_socker --hive-import --hive-table cx_hive_socker --delete-target-dir --fields-terminated-by "," -m 1 --as-textfile

sqoop command to import the data table from the MySQL database to the HBase table:
sqoop import --connect jdbc:mysql://116.63.197.140:3306/rdsdb --username root --password xxx --table 'cx_ socker', --hbase-table 'cx_hbase_socker' --column-family info --hbase-row-key timestr --hbase-create-table --m 1

    """)