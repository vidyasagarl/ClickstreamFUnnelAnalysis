create table dim_time(
time_key nvarchar(20) Primary key,
time_hour nvarchar(10),
time_second int,
time_minutes int,
timezone varchar(20)
);

