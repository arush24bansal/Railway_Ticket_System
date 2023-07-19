# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import os
import mysql.connector
from mysql.connector import Error
import Core.queries.create_queries as q
import Core.utils as u


def setup():
    
    # Accessing Server and creating databse
    server = create_connection("localhost", "root", "1804")
    create_database(server, "railway")
    server.close()
    
    # Creating Database Connection
    database = create_connection("localhost", "root", "1804", "railway")
    create_tables(database)
    
    u.print_success("SET UP COMPLETE")
    
    return database

# Helper Functions   
# =============================================================================

def create_connection(hostname, username, user_pwd, db_name=False):
    connection = None
    try:
        connection = mysql.connector.connect(
          host=hostname,
          user=username,
          password=user_pwd,
          database= db_name if db_name else None
        )
        print(f"{'Database' if db_name else 'Server'} Connection Successfull")
    except Error as err:
        u.exitHandler(False, connection, err)
    return connection



def create_database(connection, db_name):
    cursor = connection.cursor()
        
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print("Database created successfully")
    except Error as err:
        if err.errno != 1007:
            u.exitHandler(cursor, connection, err)
    cursor.close()
        
    
    
def create_tables(connection):
    cursor = connection.cursor()
    
    tables = [q.create_trains, "trains",
              q.create_stations, "stations",
              q.create_routes, "routes",
              q.create_members, "members",
              q.create_bookings, "bookings"]
    
    data_tables = ["trains", "stations", "routes"]
    
    for i in range(0, len(tables), 2):
        try:
            cursor.execute(tables[i])
            if tables[i+1] in data_tables:
                print(f"populating {tables[i+1]}. This may take a while")
                populate_table(connection, tables[i+1])
            print(f"{tables[i+1]} table created")
        except Error as err:
            if err.errno != 1050:
                u.exitHandler(cursor, connection, err)
    cursor.close()


def populate_table(connection, tableName):
    cursor = connection.cursor()
    
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    path = path.replace("Core", "Assets")
    
    try:
        with open(f"{path}\\{tableName}.csv", mode='r') as file:
            csvReader = csv.reader(file)
            headers = next(csvReader)
            insert = f"INSERT INTO {tableName}({', '.join(headers)}) VALUES("
            for row in csvReader:
                values = map(lambda x: f"'{x}'", row)
                try:
                    cursor.execute(insert + ", ".join(values) + ")")
                except Error as err:
                    cursor.execute(f"DROP TABLE {tableName}")
                    u.exitHandler(cursor, connection, err)
    except IOError as err:
        cursor.execute(f"DROP TABLE {tableName}")
        u.exitHandler(cursor, connection, err)
        
    connection.commit()
    cursor.close()