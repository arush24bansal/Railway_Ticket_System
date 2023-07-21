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
    
    functions = [train_search, h.history, h.cancel]
    
    while True:
        # Print Home Structure
        u.print_header("Home")
        print("1. Find a Train")
        print("2. Booking History")
        print("3. Cancel Ticket")
        print("4. Logout")
        u.print_prompt("Enter Serial Number of action.\nLeave blank to exit.")
        
        # Action Input
        while True:
            action = input("Action: ")
            
            if action.isspace() or action == "":
                return False
            
            if action == "4":
                return True
            
            if action.isnumeric() and int(action) in range(1, 4):
                break
            
            u.print_error("Invalid Action.", retry=True)   
            
        functions[int(action) - 1](connection, member_id)
    
     
# Train Search Functions
# =============================================================================    

def train_search(connection, member_id):
    
    u.print_header("Search Trains")
    while True:
        # Get Source
        src = get_station("source", connection)
        # Get Destination
        dest = get_station("destination", connection, src)
        # Get Date
        dateVal = get_date()
        # get Train
        train = get_train(connection, src, dest, dateVal)
        if train == 0:
            return
        elif train == 1:
            continue
        
        # Check Availability
        status = get_status(connection, train)
        print(status)
        # Input number of tickets and book




# Get Stations
# =============================================================================       
def get_station(point, connection, source=False):
    
    u.print_prompt(f"Enter search keyword for {point} station.")
    
    while True:
        # Input and Validate Keyword
        keyword = input(f"{point}: ")
        
        if not keyword.isalpha() or len(keyword) < 3:
            u.print_error("Alphabets only. Minimum 3 letters.", retry=True)
            continue
        
        # Query on Keyword
        cursor = connection.cursor()
        query = iq.fetch_stations(keyword)
        u.execute_query(cursor, connection, query)
        
        # Check query result
        stations = cursor.fetchall()
        cursor.close()
        
        if len(stations) == 0:
            u.print_error("No Stations Found.", retry=True)
            continue
        
        # Print Stations
        station_names = [sub[0] for sub in stations]
        for index, station in enumerate(station_names, start=1):
            print(f"{index}. {station}")
            
        # Select Station
        u.print_prompt("Enter Serial Number to select station.\n0 to change keyword")
        
        while True:
            action = input("Enter: ")
            
            if action == "0":
                u.print_prompt(f"Enter search keyword for {point} station.")
                break
            
            if action.isnumeric() and int(action) in range(1, len(station_names) + 1):
                i = int(action) - 1
                if source:
                    u.print_success(f"source: {source[0]}")
                u.print_success(f"{point}: {stations[i][0]}\n")
                return stations[i]
            
            u.print_error("Invalid Serial Number.", retry=True)
# Get Date    
# =============================================================================
def get_date():
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
        u.print_error("Invalid Date. Retry.")  
        
# Get Train
# =============================================================================

def get_train(connection, src, dest, dateVal):
    
    cursor = connection.cursor()
    query = iq.fetch_trains(src[1], dest[1], dateVal)
    u.execute_query(cursor, connection, query)
    
    # Check Query Result
    headers = [header[0] for header in cursor.description]
    trains = [dict(zip(headers,row)) for row in cursor.fetchall()]
    cursor.close()
    
    if len(trains) == 0: 
        u.print_error("No trains found. Try Again with different filters")
        return 1
    
    # Print Trains
    for train in trains:
        print()
        for i, j in train.items():
            print(f"{i}: {j}")
    
    # Select Train
    train_nums = [train['Train Number'] for train in trains]
    u.print_prompt("Enter Train Number to book.\n0 to start a new search.", back=True)
    while True:
        train_no = input("Enter: ")
        
        if train_no.isspace() or train_no == "":
            return 0
        
        if train_no == "0":
            return 1
        
        if train_no.isnumeric() and int(train_no) in train_nums:
            return list(filter(lambda x: x['Train Number'] == int(train_no), trains))[0]

        u.print_error("Invalid Train Number.", retry=True)
        
# Get Status
# =============================================================================
def get_status(connection, train):
    cursor = connection.cursor()
    query = iq.check_status(train)
    u.execute_query(cursor, connection, query)
    store = cursor.fetchall()
    cursor.close()
    return store
    