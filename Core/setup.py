# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import csv
import mysql.connector
from mysql.connector import Error
import queries as q
import os
import pandas as pd

def create_connection(hostname, username, user_pwd, *argv):
    connection = None
    try:
        if len(argv) > 0:
            connection = mysql.connector.connect(
              host=hostname,
              user=username,
              password=user_pwd,
              database=argv[0]
            )
            print("Database Connection Successfull")
        else:
            connection = mysql.connector.connect(
              host=hostname,
              user=username,
              password=user_pwd
            )
            print("Server Connection Successfull")
    except Error as err:
            print(f"error: {err}")
            sys.exit()
    return connection



def create_database(connection, db_name):
    cursor = connection.cursor()
        
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print("Database created successfully")
    except Error as err:
        if err.errno == 1007:
            print("Database already exists")
        else:
            errHandler(err, cursor, connection)
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
            if err.errno == 1050:
                print(f"{tables[i+1]} table already exists")
            else:
                errHandler(err, cursor, connection)
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
                    errHandler(err, cursor, connection)
    except IOError as err:
        cursor.execute(f"DROP TABLE {tableName}")
        errHandler(err, cursor, connection)
        
    connection.commit()
    cursor.close()


def errHandler(msg, cursor, connection):
    print(f"Error: {msg}")
    cursor.close()
    connection.close()
    sys.exit()