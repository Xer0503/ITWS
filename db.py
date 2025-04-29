from connection import connection_prod, connection_acc
def create():
    con = connection_acc()
    c = con.cursor()
    c.execute(
        """
    CREATE TABLE admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email unique,
    password VARCHAR(100),
    role VARCHAR(5)
    )
    """        
    )
    con.commit()
    con.close()

def query_items():
    con = connection_prod()

    c = con.cursor()

    c.execute("""
    SELECT * FROM items
    """
    )

    data = c.fetchall()
    con.commit()
    con.close()
    for i in data:
        print('fetch category: ', i)

    return data

def query_feedback():
    con = connection_prod()

    c = con.cursor()

    c.execute("""
    SELECT * FROM feedback
    """
    )

    data = c.fetchall()
    con.commit()
    con.close()
    for i in data:
        print('fetch feedback: ', i)

    return data

def addItems():
    con = connection_prod()
    c = con.cursor()

    c.execute("""
        INSERT INTO items (item_name, item_description, item_category, item_price, item_stock) 
        VALUES 
            ('ROG Laptop', 'Ultra Duper Smooth Gaming laptop', 'laptop', 20000.99, 35), 
            ('Digital Camera', 'Ultra Duper Smooth high Quality Photos', 'camera', 15000.20, 99),
            ('Apple Watch', 'Smart Fucking Watch', 'smartwatch', 999, 250);
        """)
    con.commit()
    con.close()

def deleteItems():
    con = connection_acc()
    c = con.cursor()

    c.execute("""
        DELETE FROM feedback WHERE id = 13
        """)
    con.commit()
    con.close()

def dropTable():
    con = connection_acc()
    c = con.cursor()

    c.execute("""
        DROP TABLE admin
        """)
    con.commit()
    con.close()

def query_customer():
    con = connection_acc()
    c = con.cursor()
    sql = 'SELECT * FROM admin'
    c.execute(sql)

    customer = c.fetchall()
    con.commit()
    con.close()

    for i in customer:
        print('fetch customer: ', i)

def addColumn():
    con = connection_prod()
    c = con.cursor()

    c.execute("""
        ALTER TABLE items ADD COLUMN timestamp DATETIME
    """)
    con.commit()
    con.close()

def addAdmin():
    con = connection_acc()
    c = con.cursor()

    c.execute("""
        INSERT INTO admin (first_name, last_name, email, password, role) 
        VALUES 
            ('Rexie', 'Villanueva', 'rexie03@gmail.com', 'rexie', 'admin')
              
        """)
    con.commit()
    con.close()
    
query_customer()