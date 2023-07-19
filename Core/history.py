# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:47:56 2023

@author: Arush
"""

import Core.utils as u
import Core.queries.interface_queries as iq
from mysql.connector import Error
import time


def history(connection, member_id):
    
    u.print_header("Bookings")
    
    # Get Bookings
    query = iq.bookings_history(member_id)
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
    except Error as err:
        u.exitHandler(cursor, connection, err)
        
    headers = [header[0] for header in cursor.description]
    bookings = [dict(zip(headers,row)) for row in cursor.fetchall()]
    cursor.close()
    
    if print_bookings(bookings):
        return True
    
    
    u.print_prompt("Press Enter to go back")
    input("")
    return True
    

def cancel(connection, member_id):
    
    u.print_header("Cancel Tickets")
    
    #Get Bookings
    query = iq.upcoming_bookings(member_id)
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
    except Error as err:
        u.exitHandler(cursor, connection, err)
        
    headers = [header[0] for header in cursor.description]
    bookings = [dict(zip(headers,row)) for row in cursor.fetchall()]
    booking_ids = [sub['Booking ID'] for sub in bookings]
    
    if print_bookings(bookings):
        return True
    
    u.print_prompt("Enter Booking ID to delete a booking.\nLeave blank to go back")
    while True:
        booking_id = input("Enter: ")
        if len(booking_id) == 0:
            return True
        elif booking_id.isnumeric() and int(booking_id) in booking_ids:
            break
        u.print_retry("Invalid booking ID!")
    
    
    query = iq.delete_booking(member_id, booking_id)
    
    try:
        cursor.execute(query)
    except Error as err:
        u.exitHandler(cursor, connection, err)
    
    connection.commit()
    u.print_success("Booking Successfully Deleted")
    cursor.close()
    return True


# Helper Function
# =============================================================================
def print_bookings(bookings):
    if len(bookings) == 0:
        u.print_prompt("No bookings to show\n")
        time.sleep(2)
        return True
    
    for booking in bookings:
        for i, j in booking.items():
            print(f"{i}: {j}")
        print()