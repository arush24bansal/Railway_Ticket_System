# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 09:56:08 2023

@author: Arush
"""
import sys
from termcolor import cprint

spacing = 2

def exitHandler(cursor, connection, msg=False):
    if msg:
        print_error(f"Error: {msg}")
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    sys.exit()
    
def print_error(err):
    cprint(err, "red", attrs=["bold"])
    
def print_retry(err):
    cprint(f"{err} Retry.", "red", attrs=["bold"])

def print_prompt(msg):
    cprint(msg, "cyan", attrs=["bold"])

def print_header(title):
    print("\n" * spacing, end="")
    cprint(f"    {title}    ", "blue", "on_white")
    
def print_success(msg):
    cprint(msg, "green", attrs=["bold"])
    
def print_title(title):
    print("\n" * spacing, end="")
    cprint(title, "magenta", attrs=["bold"])