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
from mysql.connector import Error


def interface(connection, member_id):
    
    actions = [
        "1. Find a Train",
        "2. Booking History",
        "3. Cancel Ticket",
        "4. Login From another Account",
        "5. Exit"
    ]
    
    functions = [train_search, h.history, h.cancel]
    
    while True:
        u.print_header("Home")
        
        for i in actions:
            print(i)
        u.print_prompt("Enter Serial Number of action you want to perform")
        
        while True:
            action = input("Enter: ")
            if action.isnumeric() and int(action) in range(1, len(actions) + 1):
                break
            u.print_error("Please enter valid action")
    
        if action == "4":
            return True
        elif action == "5":
            return False 
        
        if functions[int(action) - 1](connection, member_id):
            continue    
        break
    
     
# Train Search Functions
# =============================================================================    
    
def train_search(connection, member_id):
    
    u.print_header("Search Trains")
    cursor = connection.cursor()
    
    while True:
        # Get Filters
        src_id = getStation("Source", cursor, connection)
        dest_id = getStation("Destination", cursor, connection)
        dateVal = getDay()
        # Get Trains
        query = iq.fetch_trains(src_id, dest_id, dateVal)
        try:
            cursor.execute(query)
        except Error as err:
            u.exitHandler(cursor, connection, err)
        trains = cursor.fetchall()
        
        if len(trains) == 0: 
            u.print_error("No trains found. Try Again with different filters")
            
        for i in trains:
            print(i)
        
        u.print_prompt("Enter Train ID to book.\n0 to start a new search.\nLeave blank to go to Home.")       
        train_id = input("Enter: ")
        
        if train_id == "0":
            print()
            continue
        elif len(train_id) == 0:
            return True
        else:
            print("Book Tickets")



def getStation(prompt, cursor, connection):
    
    while True:
        # Get Keyword for Search
        keyword = input(f"{prompt}: ")
        
        if not keyword.isalpha() or len(keyword) < 3:
            u.print_retry("Use alphabets only. Enter minimum 3 letters.")
            continue
        
        # Query for Stations
        query = iq.fetch_stations(keyword)
        
        try:
            cursor.execute(query)
        except Error as err:
            u.exitHandler(cursor, connection, err)
        
        stations = cursor.fetchall()
        if len(stations) == 0:
            u.print_retry("No results match Keyword!")
            continue
        
        # Print Station names
        station_names = [sub[0] for sub in stations]
        for index, station in enumerate(station_names, start=1):
            print(f"{index}. {station}")
        
        # Select from the station names
        u.print_prompt("Enter Sr No. to select station.\nEnter 0 to make new search.")
        
        while True:
            
            sr_no = input("Enter: ")
            
            if sr_no == "0":
                print()
                break
            if sr_no.isnumeric() and int(sr_no) in range(1, len(station_names) + 1):
                selected_stn = stations[int(sr_no) - 1]
                u.print_success(f"{prompt}: {selected_stn[0]}\n")
                return selected_stn[1]
            else:
                u.print_retry("Invalid Sr No!")
                continue

def getDay():
    u.print_prompt("Enter Date in DD/MM/YYYY format.")
    checkString = "^(0?[1-9]|[1|2][0-9]|3[0|1])/(0?\d|1[0-2])/20\d{2}$"
    while True:
        dateVal = input("Enter:")
        if re.search(checkString, dateVal):
            d, m, y = [int(i) for i in dateVal.split("/")]
            try:
                return date(y, m, d)
            except:
                # Do Nothing
                True
        u.print_retry("Invalid Date.")
        
    
