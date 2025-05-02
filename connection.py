import sqlite3
db_prod = 'products.db'
db_acc = 'account.db'
db_order = 'order.db'
db_transaction = 'transaction.db'

def connection_prod():
    con = sqlite3.connect(db_prod)
    return con

def connection_acc():
    con = sqlite3.connect(db_acc)
    return con

def connection_order():
    con = sqlite3.connect(db_order)
    return con

def connection_cart():
    con = sqlite3.connect(db_order)
    return con

def connection_transaction():
    con = sqlite3.connect(db_transaction)
    return con