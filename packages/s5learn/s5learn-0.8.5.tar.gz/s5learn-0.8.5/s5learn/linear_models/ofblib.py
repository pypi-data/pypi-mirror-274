def ofblib():

    print("""
    
Decompress the file
unzip logs.zip

# Create the ods_start_log table.
drop table if exists batch.ods_start_log;
CREATE EXTERNAL TABLE batch.ods_start_log (`line` string)
PARTITIONED BY (`dt` string)
LOCATION '/warehouse/batch/ods/ods_start_log';

# Load the data.
load data inpath '/batch/logs/topic_start/2019 06 09' into table batch.ods_start_log
partition(dt='2019 06 09');

# Loads data script at the ODS layer.
Create the bin folder in /opt.
mkdir /opt/bin

Create a script in the /opt/bin directory.
cd /opt/bin

# Add the following content to the script:
#!/bin/bash
source /opt/client/bigdata_env
APP=batch
beeline=/opt/client/Hive/Beeline/bin/beeline
if [ n "$1" ] ;then
	do_date=$1
else
	do_date=`date d " 1 day" +%F`
fi
echo "===Log generation date: $do_date==="
sql="
load data inpath '/batch/logs/topic_start/$do_date' into table "$APP".ods_start_log
partition(dt='$do_date');
load data inpath '/batch/logs/topic_event/$do_date' into table "$APP".ods_event_log
partition(dt='$do_date');

"

$beeline e "$sql"

# Add the execution permission of the script.
chmod 777 ods_log.sh

# Use script.
./ods_log.sh 2019 06 10

# Import data to the startup table.
insert overwrite table batch.dwd_start_log
PARTITION (dt='2019 06 09')
select
get_json_object(line,'$.mid') mid_id,
get_json_object(line,'$.uid') user_id,
--email: Pay a ttention to spelling error
get_json_ob ject(line,'$.email') email,
from ods_start_log
where dt='2019 06 09';

# Complete content of the pom.xml file
<?xml version="1.0" encoding="UTF 8"?>
<project xmlns="http://maven.apache.org/POM/
xmlns:xsi="http://www.w3.org/2001/XMLSchema instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
http://maven.apache.org/xsd/maven 4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>
<groupId>com.huawei</groupId>
<artifactId>hive</artifactId>
<version>1.0-SNAPSHOT</version>
<properties>
<project.build.sourceEncoding>UTF8</project.build.sourceEncoding>
<hive.version>1.2.1</hive.version>
</properties>
<dependencies>
<!--Add Hive dependency.-->
<dependency>
<groupId>org.apache.hive</groupId>
<artifactId>hive-exec</artifactId>
<version>${hive.version}</version>
</dependency>
</dependency>
<build>
<plugins>
<plugin>
<artifactId>maven-compiler-plugin</artifactId>
<version>2.3.2</version>
<configuration>
<source>1.8</source>
<target>1.8</target>
</configuration>
</plugin>
<plugin>
<artifactId>maven-assembly-plugin</artifactId>
<configuration>
<descriptionRefs>
<descriptorRef>jar-with-dependencies</descriptorRef>
</descriptionRefs>
</configuration>
<executions>
<execution>
<id>make-assembly</id>
<phase>package</phase>
<goals>
<goal>single</goal>
</goals>
</execution>
</executions>
</plugin>
</plugins>
</build>
</project>

# Create the BaseUDF class in the com.huawei.udf package.
The code is as follows:
package com.huawei.udf;
import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.hive.ql.exec.UDF;
import org.json.JSONException;
import org.json.JSONObject;
public class BaseUDF extends UDF{
//Transfer two parameters
public String evaluate(String line, String jsonkeysString){
// 0 Create a StringBuilder as the result set
StringBuilder sb = new StringBuilder();
// 1 jsonkeysStrings. Use commas (,) to separate
String[] jsonkeys = jsonkeysString.split(",");
// 2 line server time | json
if (line== null){
return "";
}
//"\\"is an escape character.
String[] logContents = line.split("\\|");
//verify and determine.
if (logContents.length != 2 || StringUtils.isBlank(logContents[1])){
return "";
}
// 3 Create a JSON object for logContents[1].
try {
JSONObject jsonObject = new JSONObject(logContents[1]);
//4 Obtain the JSON object of the common field cm.
JSONObject cm = jsonObject.getJSONObject("cm");
//5 loop traversal
for (int i = 0; i < jsonkeys.length; i++) {
String jsonkey = jsonkeys[i];
if(cm.has(jsonkey)){
sb.append(cm.getString(jsonkey)).append("\t");
}else{
sb.append("\t");
}
}
//6 Combine event fields
sb.append(jsonObject.getString("et")).append("\t");
sb.append(logContents[0]).append("\t");
} catch (JSONException e) {
e.printStackTrace();
}
return sb.toString();
}
}

# Create a directory on HDFS.
hdfs dfs mkdir /user/hive_examples_jars

# Upload the JAR package from the local host to the HDFS distributed file system.
hdfs dfs put ./hive-1.0-SNAPSHOT.jar /user/hive_examples_jars

# Create temporary functions.
create temporary function base_analizer as 'com.huawei.udf.BaseUDF' using jar
'hdfs://hacluster/user/hive_examples_jars/hive-1.0-SNAPSHOT.jar';
create temporary function flat_analizer as 'com.huawei.udtf.EventUDTF' using jar
'hdfs://hacluster/user/hive_examples_jars/hive-1.0-SNAPSHOT.jar';

insert overwrite table batch.dwd_base_event_log
PARTITION (dt='2019 06 09')
select
split(base_analizer(line,'mid,uid,l,md,ba,email,hw,t,nw'),' t')[0] as mid_id,
split(base_analizer(line,'mid,uid,l,md,ba,email,hw,t,nw'),' t')[1] as user_id,
from ods_event_log where dt='2019-06-09' and
base_analizer(line,'mid,uid,l,md,ba,email,hw,t,nw')<>''
) sdk_log lateral view flat_analizer(ops) tmp_k as event_name, event_json;

get_json_object(event_json,'$.kv.action') action,
get_json_object(event_json,'$.kv.goodsid') goodsid

insert overwrite table batch.dws_uv_detail_day
partition(dt='2019-06-09')
select
mid_id,
concat_ws('|', collect_set(user_id)) user_id,
concat_ws('|', collect_set(lang))lang
from dwd_start_log
where dt='2019-06-09'
group by mid_id;

set hive.exec.dynamic.partition.mode=nonstrict;

insert overwrite table dws_uv_detail_wk
partition(wk_dt)
select
mid_id,
concat_ws('|', collect_set(user_id)) user_id,
date_add(next_day('2019-06-09',' MO'), 7),
date_add(next_day('2019-06-09','MO'), 1),
concat(date_add( next_day('2019-06-09','MO'), 7), '_' , date_add(next_day('2019-06-09','MO'), -1))
from dws_uv_detail_day
where dt>=date_add(next_day('2019-06-09','MO'), 7) and dt<=date_add(next_day('2019-06-09','MO'), -1)
group by mid_id;

insert into table ads_uv_count
select
'2019 06 09' dt,
if(date_add(next_day('2019-06-09','MO'), -1)='2019-06-09','Y','N'),

with
tmp_order as
(select
user_id,
count(*) order_count, from dwd_order_info oi group by user_id
), tmp_payment as
(select
user_id, sum(pi.total_amount) payment_amount, from dwd_payment_info pi
where date_format(pi.payment_time,'yyyy MM dd')='2019 06 09'
group by user_id)
insert overwrite table dws_user_action partition(dt='2019-06-09')
select
user_actions.user_id,
sum(user_actions.order_count),

select
'2019-06-09',
sum(uc.dc) sum_dc, cast(sum( uc.nmc)/sum( uc.dc)*100 as decimal(10,2)) new_m_ratio
from 
(select
day_count dc,
0 nmc from ads_uv_count
where dt='2019-06-09'
union all
select
0 dc,
new_mid_count nmc
from ads_new_mid_count
where create_date='2019-06-09'
)uc;

# Create the ads_uv_count table in MySQL.
Use batch;
DROP TABLE IF EXISTS `ads_uv_count`;
CREATE TABLE `ads_uv_count` (
dt` varchar(255) DEFAULT NULL COMMENT 'statistic data',
`visitor2order_convert_ratio` decimal(10, 2) DEFAULT NULL COMMENT 'conversion rate from
visitors to buyers',
`day_count` bigint(200) DEFAULT NULL COMMENT 'number of users on the current) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'number of daily
active users' ROW_FORMAT = Dynamic;

java jar spring boot echarts 0.0.1 SNAPSHOT.jar spring.datasource.url=jdbc:mysql://
127.0.0.1:3306/batch spring.datasource.username=root spring.datasource.password= root

    """)