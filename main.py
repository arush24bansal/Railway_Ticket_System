# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:14:27 2023

@author: Arush
"""

import Core.setup as s
import Core.login as l
import Core.menu as i

database = s.setup()

# Maintain Session
while True:
    member_id = l.auth(database)
    if i.interface(database, member_id):
        continue
    break

print("Closing Proram")
database.close()