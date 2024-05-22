def hblib():


    print("""
    
##to go to hbase client 
hbase shell

##to create table 
create 'cx_table_stu01' , 'cf1'

##to display all tables 
create 'cx_table_stu01' , 'cf1'

##to add data in a table 
put 'cx_table_stu01','20200002', 'cf1:name','hanmeimei' 
put 'cx_table_stu01','20200002', 'cf1:gender','female' 
put 'cx_table_stu01','20200002', 'cf1:age','19'

##to query data in scan mode

scan 'cx_table_stu01',{COLUMNS=>'cf1'} #Query only the data in the cf1 column family. 
scan 'cx_table_stu01',{COLUMNS=>'cf1:name'} #Query only the name information in the cf1 column family.

##to query data based on row key using get command 
get 'cx_table_stu01','20200001' 
get 'cx_table_stu01','20200001','cf1:name'

##querying data by specified creiteria
scan 'cx_table_stu01',{STARTROW=>'20200001','LIMIT'=>2,STOPROW=>'20200002'} 
scan 'cx_table_stu01',{STARTROW=>'20200001','LIMIT'=>2,COLUMNS=>'cf1:name'}

##to scan a table and display the data
scan 'cx_table_stu01'

##command to specify multiple versions to be queried
get 'cx_table_stu01','20200001',{COLUMNS=>'cf1',VERSIONS=>5}

##to view the table attributes
desc 'cx_table_stu01'

##to change the version of a table 
alter 'cx_table_stu01',{NAME=>'cf1','VERSIONS'=>5}

##to delete data from a column family
delete 'cx_table_stu01','20200002','cf1:age' 
get 'cx_table_stu01','20200002'

##to delete a row of data
deleteall 'cx_table_stu01','20200002' 
get 'cx_table_stu01','20200002'

##drop command to delete a table
disable 'cx_table_stu01' 
drop 'cx_table_stu01'

##using filters 
scan 'cx_table_stu01',{FILTER=>"ValueFilter(=,'binary:20')"} 
scan 'cx_table_stu01',{FILTER=>"ValueFilter(=,'binary:tom')"} 
scan 'cx_table_stu01',{FILTER=>"ColumnPrefixFilter('gender')"} 
scan 'cx_table_stu01',{FILTER=>"ColumnPrefixFilter('name') AND ValueFilter(=,'binary:hanmeimei')"}
    
    """)