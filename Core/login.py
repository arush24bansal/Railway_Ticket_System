# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 19:41:33 2023

@author: Arush
"""

import Core.utils as u


def auth(connection):
    
    u.print_header("Login")
    
    # Get Phone Number
    while True:
        phone = input("Mobile Number: ")
        if phone.isnumeric() and len(phone) == 10:
            break
        u.print_error("invalid mobile number!", retry=True)
    
    # Create Cursor
    cursor = connection.cursor()
    
    # Fetch User
    query = f"""
            SELECT member_id, password, member_name FROM members
            WHERE phone_no = '{phone}'
        """
    u.execute_query(cursor, connection, query)
    data = cursor.fetchone()
    
    # Authenticate
    if data:
        # Login
        headers = [header[0] for header in cursor.description]
        user = dict(zip(headers, data))
        return login(user)
    else:
        # Signup
        return signup(cursor, connection, phone)
    cursor.close()

    
# Helper Functions   
# =============================================================================


def login(user):
    while True:
        pwd = input("Enter Password: ")
    
        if pwd != user['password']:
            u.print_error("invalid Credentials!", retry=True)
            continue
        u.print_success(f"Succesfully Logged in. Welcome back {user['member_name']}")
        return user['member_id']


def signup(cursor, connection, phone):
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
    u.execute_query(cursor, connection, query)
    
    connection.commit()
    u.print_success(f"Succesfully Registered. Welcome {name}")
    return cursor.lastrowid 
    
    