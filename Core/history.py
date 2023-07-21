# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:47:56 2023

@author: Arush
"""

import Core.utils as u
import Core.queries.interface_queries as iq
import time

def history(connection, member_id):
    
    u.print_header("Bookings")
    
    # Get Bookings
    query = iq.bookings_all(member_id)
    cursor = connection.cursor()
    u.execute_query(cursor, connection, query)
    
    # Organize Data
    headers = [header[0] for header in cursor.description]
    bookings = [dict(zip(headers,row)) for row in cursor.fetchall()]
    cursor.close()
    
    # Display and Exit
    print_bookings(bookings)
    u.print_prompt("Press Enter to go back")
    input("")
    

def cancel(connection, member_id):
    
    u.print_header("Cancel Tickets")
    
    #Get Bookings
    query = iq.bookings_upcoming(member_id)
    cursor = connection.cursor()
    u.execute_query(cursor, connection, query)
      
    # Organize Data
    headers = [header[0] for header in cursor.description]
    bookings = [dict(zip(headers,row)) for row in cursor.fetchall()]
    booking_ids = [sub['Booking ID'] for sub in bookings]
    
    # Display
    if print_bookings(bookings):
        u.print_prompt("Press Enter to go back")
        input("")
    else:
        u.print_prompt("Enter Booking ID to delete a booking.", back=True)
        while True:
            booking_id = input("Action: ")
            
            if booking_id.isspace() or booking_id == "":
                return
            
            if booking_id.isnumeric() and int(booking_id) in booking_ids:
                break
            u.print_error("Invalid booking ID!", retry=True)
         
        query = iq.delete_booking(member_id, booking_id)
        u.execute_query(cursor, connection, query) 
        connection.commit()
        u.print_success("Booking Successfully Deleted")
        time.sleep(1)
        cursor.close()
   


# Helper Function
# =============================================================================
def print_bookings(bookings):
    if len(bookings) == 0:
        print("\nNo bookings to show")
        return True
    else:
        for booking in bookings:
            print()
            for i, j in booking.items():
                print(f"{i}: {j}")