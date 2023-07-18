# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:30:35 2023

@author: Arush
"""

import Core.utils as u
import Core.history as h
from termcolor import cprint
from mysql.connector import Error


def interface(connection, member_id):
    
    home_actions = [
        "1. Find a Train",
        "2. Booking History",
        "3. Cancel Ticket",
        "4. Login From another Account",
        "5. Exit"
    ]
    
    home_funcs = [
        "placeholder",
        train_search,
        h.history,
        h.cancel
    ]
    
    while True:
        cprint("\n\n\n    Home    ", "blue", "on_white")
        
        action = get_action(home_actions)
    
        if action == 4:
            return True
        elif action == 5:
            return False 
    
        if home_funcs[action](connection, member_id):
            continue    
        break
    
# Helper Functions   
# =============================================================================

def get_action(actions):
    
    for i in actions:
        print(i)
   
    while True:
        action = input("Action: ")
        if not action.isnumeric() or int(action) not in range(1, len(actions) + 1):
            cprint("Please enter valid action", "yellow", attrs=["bold"])
            continue
        return int(action)
    
        
# Train Search Functions
# =============================================================================    
    
def train_search(connection, member_id):
    
    cprint("\n\n\n    Search Trains    \n", "blue", "on_white")
    
    while True:
        src_id = getStation("Source: ", connection)
        dest_id = getStation("Destination: ", connection)
        
        query = f"""
            WITH cte AS (
                SELECT
                    r1.train_id,
                    r2.distance - r1.distance AS 'distance',
                    r1.dept_time AS 'departure',
                    r2.arr_time AS 'arrival',
                    r1.station_id AS 'dept_id',
                    r2.station_id AS 'arr_id'
                FROM routes r1
                JOIN routes r2
                ON r1.train_id = r2.train_id
                AND r1.station_id = {src_id}
                AND r2.station_id = {dest_id}
                AND r1.serial_no < r2.serial_no
            )

            SELECT * FROM cte
        """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Error as err:
            u.exitHandler(cursor, connection, err)
            
        res = cursor.fetchall()
        print(res)
        
        print("\n\nEnter Train ID to book. Enter 0 to start a new search. Leave blank to go back.")       
        train_id = input("Train ID: ")
        
        if train_id == "0":
            print("\n")
            continue
        elif len(train_id) == 0:
            return True
        else:
            print("Book Tickets")



def getStation(prompt, connection):
    
    cursor = connection.cursor()
    
    while True:
        keyword = input(prompt)
        
        if not keyword.isalpha():
            cprint("Invalid Keyword! Use alphabets only. Retry.", "red")
            continue
        
        query = f"""
            SELECT
                CONCAT(station_name, ' (', station_code, ')') AS station,
                station_id
            FROM stations 
            WHERE station_name LIKE '{keyword}%'
        """
        
        try:
            cursor.execute(query)
        except Error as err:
            u.exitHandler(cursor, connection, err)
            
        stations = cursor.fetchall()
        cursor.close()
        station_names = [sub[0] for sub in stations]
        
        if len(stations) == 0:
            cprint("No results match Keyword! Retry.", "red")
            continue
        break
    
    for index, station in enumerate(station_names, start=1):
        print(f"{index}. {station}")
    
    while True:
        sr_no = input("Enter station sr no: ")
        
        if sr_no.isnumeric() and int(sr_no) in range(1, len(station_names) + 1):
            break
        else:
            cprint("Invalid Sr No! Retry.", "red")
    selected_stn = stations[int(sr_no) - 1]
    cprint(f"{prompt} {selected_stn[0]}\n", "blue", attrs=["bold"])
    return selected_stn[1]