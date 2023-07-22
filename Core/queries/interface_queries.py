# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:51:39 2023

@author: Arush
"""

def fetch_trains(src_id, dest_id, date):
    return f"""
        WITH cte AS (
            SELECT
                src.train_no,
                dest.distance - src.distance AS 'distance',
                
                src.departure,
                src.station_id AS 'src_id',
                src.srn AS 'src_srn',
                
                dest.arrival,
                dest.station_id AS 'dest_id',
                dest.srn AS 'dest_srn',
                
                src.day AS 'src_day',
                dest.day AS 'dest_day',
                
                DATE_ADD('{date}', INTERVAL (0 - src.day) DAY)
                AS 'train_start_date',
                DATE_ADD('{date}', INTERVAL (dest.day - src.day) DAY)
                AS 'arrival_date'
            FROM routes src
            JOIN routes dest
            ON src.train_no = dest.train_no
            AND src.station_id = {src_id}
            AND dest.station_id = {dest_id}
            AND src.srn < dest.srn
        )
        
        SELECT
            c.train_no AS 'Train Number',
            CONCAT('{date} ', c.departure) AS 'Departure',
            CONCAT(c.arrival_date, ' ', arrival) AS 'Arrival',
            
            c.src_day,
            c.dest_day,
            c.src_id,
            c.src_srn,
            c.dest_id,
            c.dest_srn,
            c.train_start_date,
            c.distance
        FROM cte c
        JOIN trains t
        ON c.train_no = t.train_no
        AND t.weekday_no = WEEKDAY(train_start_date)
    """


def fetch_stations(keyword):
    return f"""
        SELECT
            CONCAT(station_name, ' (', station_code, ')') AS station,
            station_id
        FROM stations 
        WHERE station_name LIKE '{keyword}%'
    """
    
def bookings(member_id, upcoming=False):
    main = f"""
        SELECT
            b.booking_id AS 'Booking ID',
            t.train_name AS 'Train Name',
            s1.station_name AS 'Source',
            s2.station_name AS 'Destination',
            DATE_ADD(b.train_start_date, INTERVAL r.day DAY) AS 'Date of Travel',
            b.tickets AS 'Tickets',
            b.amount AS 'Amount'
        FROM bookings b
        JOIN stations s1
        ON b.source_id = s1.station_id
        JOIN stations s2
        ON b.destination_id = s2.station_id
        JOIN trains t
        ON b.train_no = t.train_no
        JOIN routes r
        ON b.train_no = r.train_no
        AND b.source_id = r.station_id
        WHERE member_id = {member_id}
    """
    
    if upcoming:
        main = main + " AND DATE(b.train_start_date) > DATE(NOW())"
    
    return main + " ORDER BY b.booking_id ASC;"



def delete_booking(member_id, booking_id):
    return f"""
    DELETE FROM bookings
    WHERE member_id = {member_id}
    AND booking_id = {booking_id}
"""

def check_status(train):
    return f"""
        WITH cte AS (
            SELECT
                b.*,
                r1.srn AS 'src_srn',
                r2.srn AS 'dest_srn'
            FROM bookings b
            JOIN routes r1
            ON b.train_no = r1.train_no
            AND b.source_id = r1.station_id
            JOIN routes r2
            ON b.train_no = r2.train_no
            AND b.destination_id = r2.station_id
            WHERE b.train_no = {train['Train Number']}
            AND train_start_date = '{train['train_start_date']}'
        )
        
        SELECT 100 - SUM(tickets) AS 'available'
        FROM cte
        WHERE src_srn < {train['dest_srn']}
        AND dest_srn > {train['src_srn']}
        GROUP BY train_no

    """

def book_ticket(train, member_id, src, dest, tickets):
    return f"""
        INSERT INTO bookings (
            member_id,
            train_no,
            train_start_date,
            source_id,
            destination_id,
            amount,
            tickets
        )
        VALUES (
            {member_id},
            {train['Train Number']},
            '{train['train_start_date']}',
            {src},
            {dest},
            {train['distance'] * 2 * tickets},
            {tickets}
        );
    """