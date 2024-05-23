def kmeans():

    print("""
    
1-2-a
source /opt/Bigdata/client/bogdata_env

2-1-a
mkdir -p /user/data
upload data to local linux '/user/data' directory
hdfs dfs -mkdir -p /user/data
hdfs dfs -put /user/data/t_trade_order.csv /user/data
hdfs dfs -ls /user/data

3-1-a
beeline
create database ods;
create database dw;
create database ads;
show databases;

3-2-a
use ods;

create table t_trade_order(
uuid string, order_no string, org_seq string, member_id string, user_id string, user_name string, user_tel string, 
head_pic_url string, member_name string, member_head_pic_url string, tel string, order_date string, pay_date string, 
order_source string, total_amount int, total_money int, pay_method string, delivery_method string, order_bonuspoint int) 
row format delimited fields terminated by ',' stored as textfile;

select * from ods.t_trade_order 

3-2-b
use dw;

create table t_member_detail(
member_id string, member_name string, member_head_pic_url string, tel string, order_bonuspoint int, uuid string)
row format delimited fields terminated by ',' stored as textfile;

select * from dw.t_member_detail

create table t_order_detail(
uuid string, order_no string, org_seq string, member_id string, order_date string, pay_date string, order_source string,
total_amount int, total_money int, pay_method string, delivery_method string)
row format delimited fields terminated by ',' stored as textfile;

select * from dw.t_order_detail

3-2-c
use ads;

create table t_member_common (
member_id string, bonuspoint int, uuid_num int)
row format delimited fields terminated by ',' stored as textfile;

select * from ads.t_member_common

create table t_order_common (
org_seq string, member_num int, uuid_num int, uuid_money int)
row format delimited fields terminated by ',' stored as textfile;

select * from ads.t_order_common

4-1-a
load data inpath '/user/data/t_trade_order.csv' into table t_trade_order;

5-a
insert overwrite table dw.t_order_detail select uuid, order_no, org_seq, member_id, order_date, 
pay_date, order_source, total_amount, total_money, case when payment_method = '0' then 'offline_payment' 
when payment_method = '1' then 'online_payment' when payment_method = '2' then 'WeChat' 
when payment_method = '3' then 'Alipay' when payment_method = '4' then 'bank card' end as pay_method,
case when delivery_method = '1' then 'walk-in pickup' when delivery_method = '2' then 'delivery service'
when delivery_method = '3' then 'express delivery' end as delivery_method from ods.t_trade_order;


5-b 
insert overwrite table dw.t_member_detail select member_id,member_name,member_head_pic_url,
tel,order_bonuspoint,uuid from ods.t_trade_order;

6-a
insert overwrite table ads.t_member_common select member_id,sum(order_bonuspoint) as bonuspoint,
count(uuid) as uuid_num from dw.t_member_detail group by member_id; 

6-1-1
select * from ads.t_member_common where member_id = 'member-0503'; 

6-b-a
insert overwrite table ads.t_order_common select org_seq, count(distinct member_id) as member_num,
count(uuid) as uuid_num,sum(total_money) as uuid_money from dw.t_order_detail group byn org_seq;

6-1-2
select * from ads.t_member_common where org_seq = '1014'; 

7-a
select member_id,bonuspoint from ads.t_member_common order by bonuspoint desc limit 10; 

7-b
select org_seq,uuid_money from ads.t_order_common order by uuid_money desc limit 10;

8-c
insert into table ads.t_order_common values('member_id', bonuspoint, uuid_num), 
    
    """)