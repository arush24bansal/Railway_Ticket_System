# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:51:39 2023

@author: Arush
"""

def fetch_trains(src_id, dest_id, date):
    return f"""
        WITH cte AS (
            SELECT
                src.train_id,
                dest.distance - src.distance AS 'distance',
                src.dept_time,
                dest.arr_time,
                src.station_id AS 'src_id',
                dest.station_id AS 'dept_id',
                DATE_ADD('{date}', INTERVAL (0 - src.journey_day) DAY)
                AS 'train_start_date',
                DATE_ADD('{date}', INTERVAL (dest.journey_day - src.journey_day) DAY)
                AS 'dest_arr_date',
                src.journey_day AS 'src_day',
                dest.journey_day AS 'dest_day'
            FROM routes src
            JOIN routes dest
            ON src.train_id = dest.train_id
            AND src.station_id = {src_id}
            AND dest.station_id = {dest_id}
            AND src.serial_no < dest.serial_no
        ), cte2 AS (
            SELECT
                c.train_id AS 'Train ID',
                t.train_no AS 'Train Number',
                CONCAT('{date} ', dept_time) AS 'Departure',
                CONCAT(c.dest_arr_date, ' ', arr_time) AS 'Arrival',
                c.train_start_date,
                c.distance,
                c.src_day,
                c.dest_day,
                t.op_days
            FROM cte c
            JOIN trains t
            ON c.train_id = t.train_id
            AND t.weekdays = WEEKDAY(train_start_date)
        )

        SELECT * FROM cte2
    """


def fetch_stations(keyword):
    return f"""
        SELECT
            CONCAT(station_name, ' (', station_code, ')') AS station,
            station_id
        FROM stations 
        WHERE station_name LIKE '{keyword}%'
    """
    
def bookings_all(member_id):
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
    
def bookings_upcoming(member_id):
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