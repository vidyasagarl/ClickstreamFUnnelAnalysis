insert into tblsession select * from (SELECT 
    @row_number:=CASE
        WHEN timestampdiff(MINUTE,convert( @prev_event ,datetime),convert(c.event_time , datetime))>60 or @prev_userid !=user_id THEN @row_number + 1
        ELSE @row_number
    END AS sessionid,
    @prev_event:= c.event_time as event_time,
    @prev_userid:= c.user_id as user_id,
    c.event_type as 'page',
    c.platform as 'platform',
    c.region as 'region',
    c.country as 'country'
FROM
   (select * from clicklogs order by event_time) c , (SELECT @prev_event:='2000:01:01 00:00:00',@row_number:=0,@prev_userid:='') as t

 ORDER BY user_id) m ;