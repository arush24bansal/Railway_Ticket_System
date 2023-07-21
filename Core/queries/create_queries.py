# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 01:35:34 2023

@author: Arush
"""

create_trains = """
    CREATE TABLE trains(
        train_no int NOT NULL,
        train_name varchar(50) NOT NULL,
        weekday varchar(15) NOT NULL,
        weekday_no int NOT NULL,
        CONSTRAINT primary_id PRIMARY KEY (train_no)
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
        train_no int NOT NULL,
        station_id int NOT NULL,
        srn int NOT NULL,
        arrival time NOT NULL,
        departure time NOT NULL,
        distance int NOT NULL,
        day int NOT NULL,
        CONSTRAINT primary_id PRIMARY KEY (train_no, station_id, srn),
        FOREIGN KEY (station_id) REFERENCES stations(station_id),
        FOREIGN KEY (train_no) REFERENCES trains(train_no)
    )
"""

create_members = """
    CREATE TABLE members(
        member_id int NOT NULL AUTO_INCREMENT,
        member_name varchar(100) NOT NULL,
        phone_no varchar(10) NOT NULL,
        password varchar(240) NOT NULL, 
        CONSTRAINT primary_id PRIMARY KEY (member_id),
        CONSTRAINT unique_member UNIQUE (phone_no)
    )
"""

create_bookings = """
    CREATE TABLE bookings(
        booking_id int NOT NULL AUTO_INCREMENT,
        member_id int NOT NULL,
        train_no int NOT NULL,
        train_start_date date NOT NULL,
        source_id int NOT NULL,
        destination_id int NOT NULL,
        amount int NOT NULL,
        tickets int NOT NULL,
        CONSTRAINT primary_id PRIMARY KEY (booking_id),
        FOREIGN KEY (member_id) REFERENCES members(member_id),
        FOREIGN KEY (train_no) REFERENCES trains(train_no),
        FOREIGN KEY (source_id) REFERENCES stations(station_id),
        FOREIGN KEY (destination_id) REFERENCES stations(station_id)
    )
"""
