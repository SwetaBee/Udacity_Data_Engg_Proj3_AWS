# Project 3: Build an ETL pipeline for a database hosted on Redshift using Data warehouse and AWS

## Summary
* [Introduction](#Introduction)
* [Project Description and Datasets](#Project-description-and-Datasets)
* [Schema](#Schema)
* [ETL process](#ETL-process)
* [How to run](#How-to-run)
* [Project structure](#Project-structure)
--------------------------------------------

#### Introduction

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

My task is to build an ETL Pipeline that extracts their data from S3, staging it in Redshift and then transforming data into a set of Dimensional and Fact Tables for their Analytics Team to continue finding Insights to what songs their users are listening to.

#### Project Description and Datasets

To build an ETL Pipeline for a database hosted on Redshift I will need to load data from S3 to staging tables on Redshift and execute SQL Statements that create fact and dimension tables from these staging tables to create analytics (Application of Data warehouse and AWS )

<b>Project Datasets</b>

The S3 buckets consist of:
Song Data Path     -->     s3://udacity-dend/song_data
Log Data Path      -->     s3://udacity-dend/log_data
Log Data JSON Path -->     s3://udacity-dend/log_json_path.json

<b>Song Dataset</b>

The first dataset is a subset of real data from the Million Song Dataset(https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. 
For example:

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

<b>Log Dataset</b>

The second dataset consists of log files in JSON format. The log files in the dataset with are partitioned by year and month.
For example:

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

And below is an example of what a single log file, 2018-11-13-events.json, looks like.

{"artist":"Pavement", "auth":"Logged In", "firstName":"Sylvie", "gender", "F", "itemInSession":0, "lastName":"Cruz", "length":99.16036, "level":"free", "location":"Klamath Falls, OR", "method":"PUT", "page":"NextSong", "registration":"1.541078e+12", "sessionId":345, "song":"Mercy:The Laundromat", "status":200, "ts":1541990258796, "userAgent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_4...)", "userId":10}

#### Schema

A Star Schema would be required for optimized queries on song play queries

<b>Fact Table</b>

<b>songplays</b> - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

<b>Dimension Tables</b>

<b>users</b> - users in the app
user_id, first_name, last_name, gender, level

<b>songs</b> - songs in music database
song_id, title, artist_id, year, duration

<b>artists</b> - artists in music database
artist_id, name, location, lattitude, longitude

<b>time</b> - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday


<b>Create Table Schema</b>

1. Written a SQL CREATE statement for each of these tables in sql_queries.py
2. Completed the logic in create_tables.py to connect to the database and created these tables
3. Written SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. That way I can run create_tables.py whenever I want to reset my database and test my ETL pipeline.
4. Launched a redshift cluster and created an IAM role that has read access to S3.
5. Added redshift database (ENDPOINT or HOST)and IAM role info to dwh.cfg.
6. Tested by running create_tables.py and checking the table schemas in my redshift database.


#### ETL Process

1. Implemented the logic in etl.py to load data from S3 to staging tables on Redshift.
2. Implemented the logic in etl.py to load data from staging tables to analytics tables on Redshift.
3. Tested by running etl.py after running create_tables.py and running the analytic queries on my Redshift database.
4. Deleted my redshift cluster.


#### How to Run
1. To run this project I had to fill the following information, and save it as *dwh.cfg* in the project root folder.

```
[CLUSTER]
HOST=''
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_PORT=5439

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

[AWS]
KEY=
SECRET=

[DWH]
DWH_CLUSTER_TYPE       = multi-node
DWH_NUM_NODES          = 4
DWH_NODE_TYPE          = dc2.large
DWH_CLUSTER_IDENTIFIER = 
DWH_DB                 = 
DWH_DB_USER            = 
DWH_DB_PASSWORD        = 
DWH_PORT               = 5439
DWH_IAM_ROLE_NAME      = 
```


2. Run the *create_cluster* script to set up the cluster and connect to the Database for this project.

    `$ python create_cluster.py`

3. Run the *create_tables* script to set up the database staging and analytical tables after completing *sql_queries.py*

    `$ python create_tables.py`

4. Run the *etl* script to extract data from the files in S3, stage it in redshift, and finally store it in the dimensional tables.This 
   might take a few minutes.

    `$ python etl.py`
    
5. Finally, to provide example queries and results for song play analysis, examine exam.ipynb and Run 
    `$ python Test.py`
    
   *Now can delete the cluster, roles and assigned permission*    


## Project structure

This project includes five python script files:

- test.py runs a few queries on the created star schema to validate that the project has been completed successfully.
- create_cluster.py is where the AWS components for this project are created programmatically
- create_table.py is where fact and dimension tables for the star schema in Redshift are created.
- etl.py is where data gets loaded from S3 into staging tables on Redshift and then processed into the analytics tables on Redshift.
- sql_queries.py where SQL statements are defined, which are then used by etl.py, create_table.py and analytics.py.

