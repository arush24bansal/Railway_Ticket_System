# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 09:56:08 2023

@author: Arush
"""
import sys
from mysql.connector import Error
from termcolor import cprint

def exitHandler(cursor, connection, msg=False):
    if msg:
        cprint(f"Error: {msg}", "red", attrs=["bold"])
    cursor.close()
    connection.close()
    sys.exit()


# PHONE NUMBER UTILS
def get_user_phone(cursor, connection):
    while True:
        phone = input("Mobile Number: ")
    
        if not phone.isnumeric() or len(phone) != 10:
            cprint("invalid mobile number! Retry.", "red")
            continue
        break
    
    query = f"""
            SELECT member_id, phone_no, password, member_name FROM members
            WHERE phone_no = '{phone}'
        """
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return user
        else:
            return phone
    except Error as err:
        exitHandler(cursor, connection, err)
    

def get_new_password():
    cprint("Create password.only alphabets and numbers are allowed.", "blue", "on_white")
    while True:
        pwd = input("Enter Password: ")
        
        if not pwd.isalnum() or len(pwd) > 240 :
            cprint("invalid Password! Only letters and numbers allowed. Retry.", "red")
            continue
        break
    
    while True:
        pwd2 = input("Confirm Password: ")
        if pwd2 != pwd:
            cprint("Password do not match! Retry.", "red")
            continue
        break
    
    return pwd2