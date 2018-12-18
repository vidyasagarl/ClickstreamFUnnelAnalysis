
# coding: utf-8

# In[ ]:


#The first session contain aws auomation using boto3

#section 2 contains data wrangling and uploading . Further the script automates the process of report generatio


# In[ ]:



#section 1
import boto3


# In[ ]:


#create a bucket

bucketname='anaysis'


s3client = boto3.client('s3')


try:
    response = s3client.create_bucket(Bucket=bucketname,CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'
    })
    print(response)
except Exception as error:
    print(error)

    



# In[ ]:


#uploading file to s3
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket('analysis')


try:
    response=s3resource.Bucket('analysis').upload_file('BusinessIntelligenceExercise.csv','BusinessIntelligenceExercise.csv')
    print(response)
except Exception as error:
    print(error)


# In[ ]:



#creating a AWS RDS instance to work
rds = boto3.client('rds')
rds_instance=rds.describe_db_instances()


# In[ ]:



try:
    response = rds.create_db_instance(


        DBInstanceIdentifier='mysqlserver',
        AllocatedStorage=20,
        DBInstanceClass='db.t2.micro',
        Engine='mysql',
        MasterUsername='sqladmin',
        MasterUserPassword='abcde12345',
        LicenseModel='license-included')
    print(response)
except Exception as error:
    print(error)


# In[27]:


#section2:

import pandas as pd
import pymysql
import pandas.io.sql as sql
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import DATETIME


# In[29]:



#ran into issues with rds regarding uploaidng the huge .sql file to execute had to change parameters group to modify max packet size and increased timeout
# the rds was very slow compared to my local instance hence shifted to the localhost mysql instance. replcae with aws endpoint to connect
# create tables for processing
try:
    print('Creating Database')
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sagar1991$')

    cur = conn.cursor()

    cur.execute("create database analysis")
    
    conn.commit()
   
except Exception as error:
    print(error)   
    
try:
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sagar1991$',db='analysis')

    cur = conn.cursor()

    #cur.execute("drop table clicklogs;")
    cur.execute(' create table clicklogs (event_time nvarchar(30),user_id nvarchar(150),event_type nvarchar(50),platform nvarchar(50),country nvarchar(50),region nvarchar(50),device_id nvarchar(150),initial_referring_domain varchar(50));')

    conn.commit()
except Exception as error:
    print(error)   


# In[21]:


df=pd.read_csv('BusinessIntelligenceExercise.csv',encoding='utf-8')


# In[5]:


df.head(5)



# In[4]:


m='Insert into clicklogs values'
for index,row in df.iterrows():
    s=''
    for x in range(len(row)):
        s+='\'%s\','%row[x]
    s = s[:-1]
        
    m+='(%s ),'%s
m=m[:-1]+';'   


# In[5]:



f=open('insert.sql','w+')
f.write(m)
# the insert statement files can be used to load into database 
#i ran into error with timeout and max packet size which has to be edited in the settings to succesfully execute it


# In[25]:


try:
    cur.execute(m)

except Exception as error:
    print(error)   


# In[ ]:


#ideal way of representing data would be converting the data into dimensional models.


# In[14]:


#Thought process: 

#every customer logs in into his doordash applicaion. He browses around,may be shortlists a restaurant , switches between the pages back and forth
#Hence the concept of session is very important. I am assuming a customer who has not interacted with the app for next 60 mins starts a new session


# In[38]:


try:
    sessionsql=open('create_session.sql','r')
    cur.execute(sessionsql.read())
    conn.commit()
except Exception as error:
    print(error)   


# In[39]:


try:
    sessioninsert = open('session.sql','r')
    cur.execute(sessioninsert.read())
    conn.commit()
except Exception as error:
    print(error)   
# the variable 30 min can be changed in the sql for differnt values and observer the changes with respect to net conversion at each stage.


# In[41]:


try:
   
    cur.execute('select * from tblsession where user_id=\'000068b718046bbefe2a8a0f66da663e\';')
    result=cur.fetchall()
except Exception as error:
    print(error)   


# In[54]:


result=pd.read_sql('select * from tblsession where user_id=\'000068b718046bbefe2a8a0f66da663e\';',conn)


# In[55]:


result.head((20))


# In[ ]:


# as noted above the session id changes only when there is a drastic change in the eventime for the given customer.


# In[56]:


try:
    finalresult = open('funnelpercentage.sql','r')
    
    result_flow_percentage=pd.read_sql(finalresult.read(),conn)
  
except Exception as error:
    print(error) 


# In[58]:


finalresult.close()


# In[57]:


result_flow_percentage.head(10)


# In[59]:


#percentage drop off represents the ratio of sessions which did not proceed to the next step to the total number of sessions in the step


# In[60]:


#Since the session table has already dimensions in it it becomes easy for us to further filter the data and get more precise numbers for location,refference,date and time


# In[ ]:


#2. The search dimension would be placed above all the stages. The search will be a seperate dimension having keyowrd,inital reffering domain 
#could also come under the dimension.


#note i have divided my initial approach for the following 6 dimension:(userid was not a dimension because it didnot have any information to store )

#dim_date , dim_time ,dim_session,dim_location,dim_page,dim_inital_refference

#event would be a fact less fact table to which all the dimensions join.

#Due to the quantity of work involved in data wrangling i decided to base my queries out of the sessions.sql which is effectively a fact less fact table#in my case


# In[ ]:


#With the addition of search :

#there will be a search dimesion to the table we might even include initial reference within the the search dimension if they have similar attributes


#The dim_search and fact_event_search in the schema concludes the data modelling task for part 2.

