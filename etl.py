import pandas as pd
import cql_queries as queries

from cassandra.cluster import Cluster
from prettytable import PrettyTable


def create_session():
    cluster = Cluster()
    session = cluster.connect()
    session.execute(queries.create_keyspace)
    session.set_keyspace(queries.KEYSPACE_NAME)
    return session

def load_monthly_data():
    monthly_data = pd.read_csv("data/events.csv")
    not_null = monthly_data.notnull().apply(lambda x: all(x), axis=1)
    monthly_data = monthly_data.loc[not_null]
    monthly_data = monthly_data.astype({
        "artist": str,
        "auth": str,
        "firstName": str,
        "gender": str,
        "itemInSession": int,
        "lastName": str,
        "length": float,
        "level": str,
        "location": str,
        "method": str,
        "page": str,
        "registration": int,
        "sessionId": int,
        "song": str,
        "status": str,
        "ts": int,
        "userId": int
    })    
    return monthly_data

def create_table_events_by_session_item_index(session):
    session.execute(queries.create_events_by_session_item_index)
    
def insert_data_into_events_by_session_item_index(session, monthly_data):
    for event in monthly_data[queries.events_by_session_item_index_columns].values:
        row = (element for element in event)
        session.execute(queries.insert_events_by_session_item_index, row)
        
def select_examples_in_events_by_session_item_index(session):
    selected_columns = ["artist", "song", "length"]
    query = f"""
    SELECT {', '.join(selected_columns)}
    FROM events_by_session_item_index
    WHERE sessionId = 338
      AND itemInSession = 4
    """
    rows = session.execute(query)
    table = PrettyTable()
    table.field_names = selected_columns
    for row in rows:
        table.add_row([row.artist, row.song, row.length])
    print(table)

def create_table_events_by_user_session_item_index(session):
    session.execute(queries.create_events_by_user_session_item_index)
    
def insert_data_into_events_by_user_session_item_index(session, monthly_data):
    for event in monthly_data[queries.events_by_user_session_item_index_columns].values:
        row = (element for element in event)
        session.execute(queries.insert_events_by_user_session_item_index, row)
        
def select_examples_in_events_by_user_session_item_index(session):
    selected_columns = ["artist", "song", "firstName", "lastName", "itemInSession"]
    query = f"""
    SELECT {', '.join(selected_columns)}
    FROM events_by_user_session_item_index
    WHERE userId = 10
      AND sessionId = 182
    """
    rows = session.execute(query)
    table = PrettyTable()
    table.field_names = selected_columns
    for row in rows:
        table.add_row([row.artist, row.song, row.firstname, row.lastname, row.iteminsession])
    print(table)
    

def main():
    session = create_session()
    monthly_data = load_monthly_data()
    
    create_table_events_by_session_item_index(session)
    insert_data_into_events_by_session_item_index(session, monthly_data)
    select_examples_in_events_by_session_item_index(session)
    
    create_table_events_by_user_session_item_index(session)
    insert_data_into_events_by_user_session_item_index(session, monthly_data)
    select_examples_in_events_by_user_session_item_index(session)


if __name__ == "__main__":
    main()