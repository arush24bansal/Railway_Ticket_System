# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 19:41:33 2023

@author: Arush
"""

import Core.utils as u
from termcolor import cprint
from mysql.connector import Error


def auth(connection):
    
    # Get Phone Number
    phone = get_phone()
    
    # Fetch User
    user = fetch_user(connection, phone)
    print(user)
    
    if user:
        return login(user)
    else:
        return signup(connection, phone)
   

    
# Helper Functions   
# =============================================================================

def get_phone():
    while True:
        phone = input("Mobile Number: ")
    
        if not phone.isnumeric() or len(phone) != 10:
            cprint("invalid mobile number! Retry.", "red")
            continue
        return phone


def fetch_user(connection, phone):
    cursor = connection.cursor()
    
    query = f"""
            SELECT member_id, phone_no, password, member_name FROM members
            WHERE phone_no = '{phone}'
        """
        
    try:
        cursor.execute(query)
        store = cursor.fetchone()
        cursor.close()
        return store
    except Error as err:
        u.exitHandler(cursor, connection, err)


def login(user):
    while True:
        pwd = input("Enter Password: ")
    
        if pwd != user[2]:
            cprint("invalid Credentials! Retry.", "red")
            continue
        cprint(f"Succesfully Logged in. Welcome back {user[3]}", "green", attrs=["bold"])
        return user[0]


def signup(connection, phone):
    while True:
        name = input("Enter your Name: ")
        
        if not name.isalpha() :
            cprint("invalid Name! Please only enter alphabets. Retry.", "red")
            continue
        break
    while True:
        pwd = input("Create Password: ")
        
        if not pwd.isalnum() or len(pwd) > 240  :
            cprint("invalid Password! Please enter alphabets and numbers only. Retry.", "red")
            continue
        break
    
    query = f"""
        INSERT INTO members(phone_no, member_name, password)
        VALUES('{phone}', '{name}', '{pwd}')
    """
    
    cursor = connection.cursor()
    
    try: 
        cursor.execute(query)
        connection.commit()
        store = cursor.lastrowid 
        cursor.close()
        cprint(f"Succesfully Registered. Welcome {name}", "green", attrs=["bold"])
        return store
    except Error as err: 
        u.exitHandler(cursor, connection, err)