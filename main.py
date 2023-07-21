# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:14:27 2023

@author: Arush
"""

import Core.setup as s
import Core.login as l
import Core.menu as i
import Core.utils as u

database = s.setup()

u.print_title("Welcome to Indian Railways Reservation system")

# Maintain Session
while True:
    member_id = l.auth(database)
    if i.home(database, member_id):
        continue
    break

u.print_prompt("Closing Program")
database.close()