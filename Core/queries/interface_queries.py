# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:51:39 2023

@author: Arush
"""

def fetch_trains(src_id, dest_id):
    return f"""
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


def fetch_stations(keyword):
    return f"""
        SELECT
            CONCAT(station_name, ' (', station_code, ')') AS station,
            station_id
        FROM stations 
        WHERE station_name LIKE '{keyword}%'
    """
    
def bookings_history(member_id):
    return f"""
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
    
def upcoming_bookings(member_id):
    return  f"""
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

def delete_booking(member_id, booking_id):
    return f"""
    DELETE FROM bookings
    WHERE member_id = {member_id}
    AND booking_id = {booking_id}
"""