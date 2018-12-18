drop table tblsession;

create table tblsession(
sessionid text,
event_time  nvarchar(60),
user_id nvarchar(150),
event_type nvarchar(30),
platform nvarchar(20),
region nvarchar(30),
country nvarchar(30));