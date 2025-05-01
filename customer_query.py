from connection import connection_acc

def customer_query():
    con = connection_acc()
    c = con.cursor()
    sql = 'SELECT * FROM customer'
    c.execute(sql)
    
    customer = c.fetchall()
    con.commit()
    con.close()

    return customer

def active_customer():
    con = connection_acc()
    c = con.cursor()
    sql = 'SELECT * FROM customer WHERE is_active = 1'
    c.execute(sql)
    
    customer = c.fetchall()
    con.commit()
    con.close()

    return customer