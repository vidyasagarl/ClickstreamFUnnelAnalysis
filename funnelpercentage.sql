select f.*,(f.`prevsession Total`-f.`sessionTotal`)/f.`prevsession Total` as 'percent dropoff at stage',f.sessionTotal/f.`Total sessions` as 'Net Flow percentage' from (

select k.event_type as 'Page',count(distinct sessionid) as 'sessionTotal',t.Total as 'prevsession Total' ,r.Total as 'Total sessions'
from tblsession k ,
(select count(distinct sessionid) as'Total'  from tblsession m)t ,(select count(distinct sessionid) as'Total'  from tblsession m)r
where rtrim(ltrim(k.event_type)) = 'home_page' 

union

select k.event_type as 'Page',count(distinct sessionid) as 'sessionTotal',t.Total as 'prevsession Total',r.Total as 'Total sessions'
from tblsession k ,
(select count(distinct sessionid) as'Total'  from tblsession m 
where rtrim(ltrim(m.event_type)) = 'home_page'  )t,(select count(distinct sessionid) as'Total'  from tblsession m)r
 where rtrim(ltrim(k.event_type)) = 'store_ordering_page' 

union

select k.event_type as 'Page',count(distinct sessionid) as 'sessionTotal',t.Total as 'prevsession Total',r.Total as 'Total sessions'
from tblsession k ,
(select count(distinct sessionid) as'Total'  from tblsession m 
where rtrim(ltrim(m.event_type)) = 'store_ordering_page'  )t ,(select count(distinct sessionid) as'Total'  from tblsession m)r 
where rtrim(ltrim(k.event_type)) = 'checkout_page' 

union

select k.event_type as 'Page',count(distinct sessionid) as 'sessionTotal',t.Total as 'prevsession Total',r.Total as 'Total sessions'
from tblsession k ,
(select count(distinct sessionid) as'Total'  from tblsession m
 where rtrim(ltrim(m.event_type)) = 'checkout_page'  )t,(select count(distinct sessionid) as'Total'  from tblsession m)r 
 where rtrim(ltrim(k.event_type)) = 'checkout_success' 
)f;


