create table event_fact(
eventid nvarchar(20) primary key,
sessionID nvarchar(30),
device_id nvarchar(150),
user_id nvarchar(150),
reference_fk_id nvarchar(40),
location_fk_id nvarchar(30),
page_fk_id nvarchar(50),
date_key nvarchar(30),
time_key nvarchar(20)
);

alter table event_fact add
CONSTRAINT const_fk_reference
FOREIGN KEY fk_reference (reference_fk_id)
REFERENCES dim_reference(reffernce_id);

alter table event_fact add
CONSTRAINT const_fk_location
FOREIGN KEY fk_location (location_fk_id)
REFERENCES dim_location(location_id);

alter table event_fact add
CONSTRAINT const_fk_page
FOREIGN KEY fk_page (page_fk_id)
REFERENCES dim_page(page_id);

alter table event_fact add
CONSTRAINT const_fk_time
FOREIGN KEY fk_time (time_key)
REFERENCES dim_time(time_key);


alter table event_fact add
CONSTRAINT const_fk_date
FOREIGN KEY fk_date (date_key)
REFERENCES dim_date(dateID)
;