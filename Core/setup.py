# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import csv
import mysql.connector
from mysql.connector import Error
import Core.create_queries as q
import Core.utils as u
import os
from termcolor import cprint

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
            cprint("Database Connection Successfull", "blue", "on_white")
        else:
            connection = mysql.connector.connect(
              host=hostname,
              user=username,
              password=user_pwd
            )
            cprint("Server Connection Successfull", "blue", "on_white")
    except Error as err:
            print(f"error: {err}")
            sys.exit()
    return connection



def create_database(connection, db_name):
    cursor = connection.cursor()
        
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")
        cprint("Database created successfully", "blue", "on_white")
    except Error as err:
        if err.errno == 1007:
            cprint("Database already exists", "blue", "on_white")
        else:
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
                cprint(f"populating {tables[i+1]}. This may take a while", "grey")
                populate_table(connection, tables[i+1])
            cprint(f"{tables[i+1]} table created", "blue", "on_white")
        except Error as err:
            if err.errno == 1050:
                cprint(f"{tables[i+1]} table already exists", "blue", "on_white")
            else:
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