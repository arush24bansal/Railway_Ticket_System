# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 01:35:34 2023

@author: Arush
"""

create_trains = """
    CREATE TABLE trains(
        train_id int NOT NULL,
        train_no varchar(30) NOT NULL,
        train_name varchar(50) NOT NULL,
        op_days varchar(15),
        CONSTRAINT unique_train UNIQUE (train_no),
        CONSTRAINT primary_id PRIMARY KEY (train_id)
    )
"""

create_stations =  """
    CREATE TABLE stations(
        station_id int NOT NULL,
        station_code varchar(10) NOT NULL,
        station_name varchar(60) NOT NULL,
        CONSTRAINT unique_station UNIQUE (station_code),
        CONSTRAINT primary_id PRIMARY KEY (station_id)
    )
"""

create_routes = """
    CREATE TABLE routes(
        train_id int NOT NULL,
        station_id int NOT NULL,
        serial_no int NOT NULL,
        arr_time time NOT NULL,
        dept_time time NOT NULL,
        distance int NOT NULL,
        journey_day int NOT NULL,
        CONSTRAINT primary_id PRIMARY KEY (train_id, station_id, serial_no),
        FOREIGN KEY (station_id) REFERENCES stations(station_id),
        FOREIGN KEY (train_id) REFERENCES trains(train_id)
    )
"""

create_members = """
    CREATE TABLE members(
        member_id int NOT NULL AUTO_INCREMENT,
        phone_no varchar(10) NOT NULL,
        member_name varchar(100) NOT NULL,
        password varchar(240) NOT NULL, 
        CONSTRAINT primary_id PRIMARY KEY (member_id),
        CONSTRAINT unique_member UNIQUE (phone_no)
    )
"""

create_bookings = """
    CREATE TABLE bookings(
        booking_id int NOT NULL,
        member_id int NOT NULL,
        train_id int NOT NULL,
        train_start_date date NOT NULL,
        src_station_id int NOT NULL,
        dest_station_id int NOT NULL,
        amount int NOT NULL,
        no_of_tickets int NOT NULL,
        CONSTRAINT primary_id PRIMARY KEY (booking_id),
        FOREIGN KEY (member_id) REFERENCES members(member_id),
        FOREIGN KEY (train_id) REFERENCES trains(train_id),
        FOREIGN KEY (src_station_id) REFERENCES stations(station_id),
        FOREIGN KEY (dest_station_id) REFERENCES stations(station_id)
    )
"""
