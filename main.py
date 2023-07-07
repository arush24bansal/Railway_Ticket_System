# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:14:27 2023

@author: Arush
"""

import Core.setup as s
import Core.interface as i

# Establishing Connection with the server
server_con = s.create_connection("localhost", "root", "1804")
# Creating the database
s.create_database(server_con, "railway")
# Close server connection
server_con.close()
# Connecting to the database in the server
db_con = s.create_connection("localhost", "root", "1804", "railway")
# Create and Populate Tables
s.create_tables(db_con)

# ============ SETUP COMPLETE ============



# Close Server Connection
db_con.close()
