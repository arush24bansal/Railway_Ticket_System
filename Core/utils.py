# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 09:56:08 2023

@author: Arush
"""
import sys
from termcolor import cprint

def exitHandler(cursor, connection, msg=False):
    if msg:
        cprint(f"Error: {msg}", "red", attrs=["bold"])
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    sys.exit()