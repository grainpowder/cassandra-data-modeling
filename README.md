# Sparkify Play Event Log Data Modeling

An imaginary startup company Sparkify provides music streaming service, and has been stored streaming history as CSV file format for a long time. This prevented their data analyst and data science team from utilizing this data, since information in individual file cannot be easily queried. However, amount of their streaming log data stored every second is too much to handle with relational database. Therefore, data engineer decided to store data in Apache Cassandra NoSQL database for following purposes:

1. Horizontal scale-up for massive data storage
1. High throughput for real-time music recommendation

## Repository

* `preprocess.py`: aggregates multiple log data csv files into single csv file
* `cql_queries.py`: Cassandra query used to execute ETL jobs defined in following module
* `etl.py`: actual module that contains logic on main routine to perform ETL jobs

## Execute

```shell
python preprocess.py
python etl.py
```

By executing `preprocess.py`, log data files stored in `data` directory are aggregated as single `events.csv` file in the same directory. From there, `etl.py` creates two denormalized tables to store pre-joined information and inserts corresponding data into the table. More specifically, this module stores streaming event log data as described below.

### Events partitioned by session and items played within

Combination of session and items played within can be used to uniquely identify each individual row. Therefore, `sessionId` and `itemInSession` columns are set as primary key of the table. 

```sql
CREATE TABLE IF NOT EXISTS events_by_session_item_index (
    sessionId int,
    itemInSession int,
    artist text,
    song text,
    length double,
    PRIMARY KEY (sessionId, itemInSession)
)
```

As a result, data inserted in this table is filtered and conditioned by `WHERE` clause using values on these primary keys. 

```sql
SELECT artist, song, length
FROM events_by_session_item_index
WHERE sessionId = 338
  AND itemInSession = 4
```

```
+-----------+---------------------------------+----------+
|   artist  |               song              |  length  |
+-----------+---------------------------------+----------+
| Faithless | Music Matters (Mark Knight Dub) | 495.3073 |
+-----------+---------------------------------+----------+
```

### Events partitioned by users and sessions they created

Combination of user, session and item index in each session that each user had generated can make each listening event unique. Therefore, `userId`, `sessionId` and `itemInSession` columns are set as primary key of the table. Especially, `itemInSession` column is set as clustering column to fix ordering of the stored data as ascending order of this column.

```sql
CREATE TABLE IF NOT EXISTS events_by_user_session_item_index (
    userId int, 
    sessionId int, 
    itemInSession int,
    artist text,
    song text,
    firstName text,
    lastName text,    
    PRIMARY KEY ((userId, sessionId), itemInSession)
)
```

As a result, data inserted in this table is filtered and conditioned by `WHERE` clause using values on these primary keys. 

```sql
SELECT artist, song, firstName, lastName, itemInSession
FROM events_by_user_session_item_index
WHERE userId = 10
  AND sessionId = 182
```

```
+-------------------+-------------------------------------+-----------+----------+---------------+
|       artist      |                 song                | firstName | lastName | itemInSession |
+-------------------+-------------------------------------+-----------+----------+---------------+
|  Down To The Bone |          Keep On Keepin' On         |   Sylvie  |   Cruz   |       0       |
|    Three Drives   |             Greece 2000             |   Sylvie  |   Cruz   |       1       |
| Sebastien Tellier |              Kilometer              |   Sylvie  |   Cruz   |       2       |
|   Lonnie Gordon   | Catch You Baby (Steve Pitron & ...) |   Sylvie  |   Cruz   |       3       |
+-------------------+-------------------------------------+-----------+----------+---------------+
```