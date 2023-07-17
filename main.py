# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:14:27 2023

@author: Arush
"""

import Core.setup as s
import Core.login as l

database = s.setup()
member_id = l.auth(database)
print(member_id)

print("Closing Connection")
database.close()