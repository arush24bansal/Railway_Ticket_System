# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:30:35 2023

@author: Arush
"""

import Core.utils as u
import time
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
        history,
        cancel
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
    
    cprint("\n\n\n    Search Trains    ", "blue", "on_white")
    
    search_actions = [
        "1. Book",
        "2. Search Again",
        "3. Back"
    ]    
        
    action = get_action(search_actions)
    
    if action == 3:
        return True

# History Function
# =============================================================================

def history(connection, member_id):
    
    cprint("\n\n\n    Bookings    \n", "blue", "on_white")
    
    query = f"""
        SELECT
            b.booking_id AS 'Booking ID',
            t.train_name AS 'Train Name',
            s1.station_name AS 'Source',
            s2.station_name AS 'Destination',
            b.no_of_tickets AS 'Tickets',
            b.amount AS 'Amount'
        FROM bookings b
        JOIN stations s1
        ON b.src_station_id = s1.station_id
        JOIN stations s2
        ON b.dest_station_id = s2.station_id
        JOIN trains t
        ON b.train_id = t.train_id
        WHERE member_id = {member_id}
        ORDER BY b.booking_id ASC
    """
    
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
    except Error as err:
        u.exitHandler(cursor, connection, err)
        
    headers = [header[0] for header in cursor.description]
    bookings = [dict(zip(headers,row)) for row in cursor.fetchall()]
    cursor.close()
    
    if len(bookings) == 0:
        print("No Bookings to show\n")
        time.sleep(3)
        return True
    
    for booking in bookings:
        for i, j in booking.items():
            print(f"{i}: {j}")
        print()
    print("Press Enter to go back", end="")
    input("")
    return True

# Cancel Function
# =============================================================================    

def cancel(connection, member_id):
    
    cprint("\n\n\n    Cancel Tickets    \n", "blue", "on_white")
    
    query = f"""
        SELECT
            b.booking_id AS 'Booking ID',
            t.train_name AS 'Train Name',
            s1.station_name AS 'Source',
            s2.station_name AS 'Destination',
            b.no_of_tickets AS 'Tickets',
            b.amount AS 'Amount'
        FROM bookings b
        JOIN stations s1
        ON b.src_station_id = s1.station_id
        JOIN stations s2
        ON b.dest_station_id = s2.station_id
        JOIN trains t
        ON b.train_id = t.train_id
        WHERE member_id = {member_id}
        AND DATE(b.train_start_date) > DATE(NOW())
        ORDER BY b.booking_id ASC
    """

    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
    except Error as err:
        u.exitHandler(cursor, connection, err)
        
    headers = [header[0] for header in cursor.description]
    bookings = [dict(zip(headers,row)) for row in cursor.fetchall()]
    booking_ids = [sub['Booking ID'] for sub in bookings]
    
    if len(bookings) == 0:
        print("No Upcoming Travels to show\n")
        time.sleep(2)
        return True
    for booking in bookings:
        for i, j in booking.items():
            print(f"{i}: {j}")
        print()
    print("Enter Booking ID to delete a booking. Leave blank to go back")
    while True:
        booking_id = input("Booking ID: ")
        if len(booking_id) == 0:
            return True
        elif booking_id.isnumeric() and int(booking_id) in booking_ids:
            break
        cprint("Invalid booking ID! retry.", "red")
    
    
    query = f"""
        DELETE FROM bookings
        WHERE member_id = {member_id}
        AND booking_id = {booking_id}
    """
    
    try:
        cursor.execute(query)
        connection.commit()
        cprint("Booking Successfully Deleted", "green", attrs=["bold"])
    except Error as err:
        u.exitHandler(cursor, connection, err)
        
    cursor.close()
    return True


