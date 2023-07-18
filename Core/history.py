# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:47:56 2023

@author: Arush
"""

import Core.utils as u
import time
from termcolor import cprint
from mysql.connector import Error

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
        time.sleep(2)
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