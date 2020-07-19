import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplays_table_drop = "DROP TABLE IF EXISTS songplays_table"
user_table_drop = "DROP TABLE IF EXISTS users_table"
song_table_drop = "DROP TABLE IF EXISTS songs_table"
artist_table_drop = "DROP TABLE IF EXISTS artists_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events_table(
                                artist TEXT,
                                auth TEXT,
                                first_name TEXT,
                                gender CHAR,
                                item_inSession INTEGER,
                                last_name TEXT,
                                length FLOAT,
                                level TEXT,
                                location TEXT,
                                method TEXT,
                                page TEXT,
                                registration FLOAT,
                                session_ID INTEGER,
                                song TEXT,
                                status INTEGER,
                                ts TIMESTAMP,
                                user_agent TEXT,
                                user_ID INTEGER )
""")

staging_songs_table_create = ("""CREATE  TABLE IF NOT EXISTS staging_songs_table(
                                num_songs INTEGER,
                                artist_ID TEXT,
                                artist_latitude FLOAT,
                                artist_longitude FLOAT,
                                artist_location TEXT,
                                artist_name TEXT,
                                song_ID TEXT,
                                title TEXT,
                                duration FLOAT,
                                year INTEGER)
""")

songplays_table_create = ("""CREATE TABLE IF NOT EXISTS songplays_table(
                            songplays_ID INT IDENTITY(1,1) PRIMARY KEY,
                            start_time TIMESTAMP SORTKEY DISTKEY,
                            user_ID INTEGER NOT NULL,
                            level TEXT,
                            song_ID TEXT,
                            artist_ID TEXT,
                            session_ID INTEGER,
                            location TEXT,
                            user_agent TEXT)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users_table(
                        user_ID INTEGER SORTKEY PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        gender CHAR,
                        level TEXT)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs_table(
                        song_ID TEXT SORTKEY PRIMARY KEY,
                        title TEXT,
                        artist_ID TEXT,
                        year INTEGER,
                        duration FLOAT )
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists_table(
                          artist_ID TEXT SORTKEY PRIMARY KEY,
                          name TEXT,
                          location TEXT,
                          latitude FLOAT,
                          longitude FLOAT )
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table(
                        start_time TIMESTAMP   SORTKEY DISTKEY PRIMARY KEY,
                        hour INTEGER,
                        day INTEGER,
                        week INTEGER,
                        month INTEGER,
                        year INTEGER,
                        weekDay INTEGER  )
""")

# STAGING TABLES

LOG_DATA = config['S3']['LOG_DATA']
SONG_DATA = config['S3']['SONG_DATA']
IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_JSON_PATH = config['S3']['LOG_JSONPATH']

#print('LOG_JSONPATH')

staging_events_copy = ("""copy staging_events_table 
                          from {}
                          credentials 'aws_iam_role={}'
                          COMPUPDATE OFF region 'us-west-2'
                          TIMEFORMAT as 'epochmillisecs'
                          TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
                          FORMAT AS json {}; 
""").format(LOG_DATA, IAM_ROLE, LOG_JSON_PATH)

staging_songs_copy = ("""copy staging_songs_table 
                          from {} 
                          CREDENTIALS 'aws_iam_role={}'
                          COMPUPDATE OFF region 'us-west-2'
                          TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
                          FORMAT AS json 'auto';
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES

songplays_table_insert = (""" INSERT INTO songplays_table (start_time, user_ID, level, song_ID, artist_ID, session_ID, location, user_agent)
    SELECT  DISTINCT
            e.ts            AS start_time, 
            e.user_ID       AS user_ID, 
            e.level         AS level, 
            s.song_ID       AS song_ID, 
            s.artist_ID     AS artist_ID, 
            e.session_ID    AS session_ID, 
            e.location      AS location, 
            e.user_agent    AS user_agent
    FROM staging_events_table e
    JOIN staging_songs_table  s   ON (e.song = s.title AND e.artist = s.artist_name)
    AND e.page  =  'NextSong'
""")

user_table_insert = ("""INSERT INTO users_table(user_ID, first_name, last_name, gender, level)
                        SELECT DISTINCT  user_ID, first_name, last_name, gender, level
                        FROM staging_events_table
                        WHERE page = 'NextSong'
""")

song_table_insert = ("""INSERT INTO songs_table(song_ID, title, artist_ID, year, duration)
                        SELECT song_ID, title, artist_ID, year, duration
                        FROM staging_songs_table
                        WHERE song_ID IS NOT NULL
""")

artist_table_insert = ("""INSERT INTO artists_table(artist_ID, name, location, latitude, longitude)
                          SELECT DISTINCT artist_ID, artist_name, artist_location , artist_latitude, artist_longitude 
                          FROM staging_songs_table
                          WHERE artist_ID IS NOT NULL
""")

time_table_insert = ("""INSERT INTO time_table (start_time, hour, day, week, month, year, weekday)
    SELECT  DISTINCT(start_time)                AS start_time,
            EXTRACT(hour FROM start_time)       AS hour,
            EXTRACT(day FROM start_time)        AS day,
            EXTRACT(week FROM start_time)       AS week,
            EXTRACT(month FROM start_time)      AS month,
            EXTRACT(year FROM start_time)       AS year,
            EXTRACT(dayofweek FROM start_time)  as weekday
    FROM songplays_table;
""")

# GET LIST FROM EACH TABLE
LIST_staging_events = ("""
    SELECT COUNT(*) FROM staging_events_table
""")

LIST_staging_songs = ("""
    SELECT COUNT(*) FROM staging_songs_table
""")

LIST_songplays = ("""
    SELECT COUNT(*) FROM songplays_table
""")

LIST_users = ("""
    SELECT COUNT(*) FROM users_table
""")

LIST_songs = ("""
    SELECT COUNT(*) FROM songs_table
""")

LIST_artists = ("""
    SELECT COUNT(*) FROM artists_table
""")

LIST_time = ("""
    SELECT COUNT(*) FROM time_table
""")

# QUERY LISTS

# create_table_queries = [staging_events_table_create, staging_songs_table_create, songplays_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplays_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
create_table_queries = [songplays_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplays_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplays_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
select_table_queries= [LIST_staging_events, LIST_staging_songs, LIST_songplays, LIST_users, LIST_songs, LIST_artists, LIST_time]
