from typing import List


KEYSPACE_NAME = "sparkify_log_db"

drop_keyspace = f"DROP KEYSPACE IF EXSISTS {KEYSPACE_NAME}"
create_keyspace = f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE_NAME}"
create_keyspace += " WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}"

# CQL related to table made to query event log by sessionId and itemInSession

create_events_by_session_item_index = """
CREATE TABLE IF NOT EXISTS events_by_session_item_index (
    sessionId int,
    itemInSession int,
    artist text,
    song text,
    length double,
    PRIMARY KEY (sessionId, itemInSession)
)
"""
events_by_session_item_index_columns = [
    "sessionId", "itemInSession", "artist", "song", "length"
]
insert_events_by_session_item_index = f"""
INSERT INTO events_by_session_item_index (
    {', '.join(events_by_session_item_index_columns)}
)
VALUES (%s, %s, %s, %s, %s)
"""
drop_events_by_session_item_index = """
DROP TABLE IF EXISTS events_by_session_item_index
"""

# CQL related to table made to query event log by userId, sessionId, itemInSession\
# where log is ordered by ascending itemInSession order(i.e. clustering column)

create_events_by_user_session_item_index = """
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
"""
events_by_user_session_item_index_columns = [
    "userId", "sessionId", "itemInSession", "artist", "song", "firstName", "lastName"
]
insert_events_by_user_session_item_index = f"""
INSERT INTO events_by_user_session_item_index (
    {', '.join(events_by_user_session_item_index_columns)}
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
drop_events_by_user_session_item_index = """
DROP TABLE IF EXISTS events_by_user_session_item_index
"""
