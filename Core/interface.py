# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 19:41:33 2023

@author: Arush
"""

import Core.utils as u
from termcolor import cprint
from mysql.connector import Error


def auth(connection):
    cursor = connection.cursor()
    
    user = u.get_user_phone(cursor, connection)

    # If user already Exists, Login
    if type(user) != str:
        while True:
            pwd = input("Enter Password: ")
            
            if pwd == user[2]:
                cprint(f"Succesfully Logged in. Welcome Back {user[3]}", "green", attrs=["bold"])
                return user[0]
            else:
                cprint("Invalid Password! Retry.", "red")
                continue 
    
    # If user doesn't exist, Signup
    cprint("Welcome New User.\nPlease register.", "blue", "on_white")
    pwd = u.get_new_password()
    name = input("Enter Name: ")
    
    create_query = f"""
        INSERT INTO members(phone_no, member_name, password)
        VALUES('{user}', '{name}', '{pwd}')
    """
    
    try:
        cursor.execute(create_query)
        connection.commit()
        member_id = cursor.lastrowid 
        cursor.close()
        cprint(f"Succesfully Registered. Welcome {name}", "green", attrs=["bold"])
        return member_id
    except Error as err: 
        u.exitHandler(cursor, connection, err)