# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 09:56:08 2023

@author: Arush
"""
import sys
from termcolor import cprint
from mysql.connector import Error

spacing = 5

def exitHandler(cursor, connection, msg=False):
    if msg:
        print_error(f"Error: {msg}")
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    sys.exit()

    
def print_error(err, retry=False):
    if retry:
        err = err + " Retry."
    cprint(err, "red", attrs=["bold"])


def print_prompt(msg, back=False):
    if back:
        msg = msg + "\nLeave blank to go back"
    cprint(f"\n{msg}", "cyan", attrs=["bold"])


def print_header(title):
    print("\n" * spacing, end="")
    cprint(f"    {title}    ", "blue", "on_white")
    
    
def print_success(msg):
    cprint(msg, "green", attrs=["bold"])
    
    
def print_title(title):
    print("\n" * spacing, end="")
    cprint(title, "magenta", attrs=["bold"])
    
    
def execute_query(cursor, connection, query):
    try:
        cursor.execute(query)
    except Error as err:
        exitHandler(cursor, connection, err)
    