# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 19:41:33 2023

@author: Arush
"""

import Core.utils as u
from mysql.connector import Error


def auth(connection):
    
    u.print_header("Login")
    # Get Phone Number
    phone = get_phone()
    
    # Fetch User
    user = fetch_user(connection, phone)
    
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
            u.print_retry("invalid mobile number!")
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
    except Error as err:
        u.exitHandler(cursor, connection, err)
    
    store = cursor.fetchone()
    cursor.close()
    return store


def login(user):
    while True:
        pwd = input("Enter Password: ")
    
        if pwd != user[2]:
            u.print_retry("invalid Credentials!")
            continue
        u.print_success(f"Succesfully Logged in. Welcome back {user[3]}")
        return user[0]


def signup(connection, phone):
    while True:
        name = input("Enter your Name: ")
        
        if name.isalpha():
            break
        u.print_retry("invalid Name! Enter alphabets only.")
        
    while True:
        pwd = input("Create Password: ")
        
        if pwd.isalnum() and len(pwd) <= 240:
            break
        u.print_retry("invalid Password! Enter alphabets and numbers only.")
        
    
    query = f"""
        INSERT INTO members(phone_no, member_name, password)
        VALUES('{phone}', '{name}', '{pwd}')
    """
    
    cursor = connection.cursor()
    
    try: 
        cursor.execute(query)
    except Error as err: 
        u.exitHandler(cursor, connection, err)
    
    connection.commit()
    store = cursor.lastrowid 
    cursor.close()
    u.print_success(f"Succesfully Registered. Welcome {name}")
    return store