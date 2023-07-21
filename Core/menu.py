# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:30:35 2023

@author: Arush
"""

import re
from datetime import date
import Core.utils as u
import Core.history as h
import Core.queries.interface_queries as iq


def home(connection, member_id):
    
    actions = ["Find a Train", "Booking History", "Cancel Ticket", "Logout"]
    
    functions = [train_search, h.history, h.cancel]
    
    while True:
        u.print_header("Home")
        
        for i, j in enumerate(actions, start=1):
            print(f"{i}. {j}")
        u.print_prompt("Enter Serial Number of action.\nLeave blank to exit.")
        
        while True:
            action = input("Action: ")
            
            if action.isspace() or action == "":
                return False
            
            if action.isnumeric() and int(action) in range(1, len(actions) + 1):
                action = int(action)
                break
            
            u.print_error("Invalid Action.", retry=True)
            
        if action == 4:
            return True
        
        functions[action - 1](connection, member_id)
    
     
# Train Search Functions
# =============================================================================    
    
def train_search(connection, member_id):
    
    u.print_header("Search Trains")
    cursor = connection.cursor()
    
    while True:
        # Get Source Station
        src_id = 7358
        #getStation("Source", cursor, connection)
        if not src_id:
            return
        
        # Get Destination Station
        dest_id = 65
        #getStation("Destination", cursor, connection)
        if not dest_id:
            return
        
        # Get Travel Date
        dateVal = date(2023, 11, 24)
        #getDay()
        
        # Get Trains
        query = iq.fetch_trains(src_id, dest_id, dateVal)
        u.execute_query(cursor, connection, query)
        
        # Print Trains
        headers = [header[0] for header in cursor.description]
        trains = [dict(zip(headers,row)) for row in cursor.fetchall()]
        if len(trains) == 0: 
            u.print_error("No trains found. Try Again with different filters")
            continue
        
        # Store Train Ids
        train_ids = [train['Train ID'] for train in trains]
        print(train_ids)
        for train in trains:
            for i, j in train.items():
                print(f"{i}: {j}")
            print()
        
        u.print_prompt("Enter Train ID to book.\n0 to start a new search.\nLeave blank to go to Home.")       
        
        while True:
            train_id = input("Enter: ")
        
            if train_id == "0":
                print()
                break
            elif len(train_id) == 0:
                return True
            elif train_id.isnumeric() and int(train_id) in train_ids:
                train_data = list(filter(lambda x: x['Train ID'] == int(train_id), trains))[0]
                print(train_data)
                continue
            else:
                u.print_retry("Invalid Train ID")
                continue
            



def getStation(prompt, cursor, connection):
    
    u.print_prompt(f"Enter search keyword for {prompt} station.", back=True)
    
    while True:
        # Get Keyword for Search
        keyword = input(f"{prompt}: ")
        
        if keyword.isspace() or keyword == "":
            return False
        
        if not keyword.isalpha() or len(keyword) < 3:
            u.print_error("Use alphabets only. Enter minimum 3 letters.", retry=True)
            continue
        
        # Query for Stations
        query = iq.fetch_stations(keyword)
        u.execute_query(cursor, connection, query)
        
        #  Data 
        stations = cursor.fetchall()
        if len(stations) == 0:
            u.print_error("No Stations Found.", retry=True)
            continue
        
        # Print Station names
        station_names = [sub[0] for sub in stations]
        for index, station in enumerate(station_names, start=1):
            print(f"{index}. {station}")
        
        # Select from the station names
        u.print_prompt("Enter Sr No. to select station.")
        
        while True:
            sr_no = input("Enter: ")
            
            if sr_no.isnumeric() and int(sr_no) in range(1, len(station_names) + 1):
                selected_stn = stations[int(sr_no) - 1]
                u.print_success(f"{prompt}: {selected_stn[0]}\n")
                return selected_stn[1]
            else:
                u.print_error("Invalid Sr No.", retry=True)



def getDay():
    u.print_prompt("Enter Date in DD/MM/YYYY format.")
    checkString = "^(0?[1-9]|[1|2][0-9]|3[0|1])/(0?\d|1[0-2])/20\d{2}$"
    while True:
        dateVal = input("Enter:")
        if re.search(checkString, dateVal):
            d, m, y = [int(i) for i in dateVal.split("/")]
            try:
                
                input_date = date(y, m, d)
                today = date.today()
                if input_date >= today:
                    u.print_success(f"date: {input_date}\n")
                    return input_date
            except:
                # Do Nothing
                True
        u.print_retry("Invalid Date.")
        
    
