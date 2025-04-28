import sqlite3
db_prod = 'products.db'
db_acc = 'account.db'

def connection_prod():
    con = sqlite3.connect(db_prod)
    return con

def connection_acc():
    con = sqlite3.connect(db_acc)
    return con