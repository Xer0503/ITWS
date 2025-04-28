from connection import connection_prod, connection_acc
def create():
    con = connection_acc()
    c = con.cursor()
    c.execute(
        """
    CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    contacts VARCHAR(12),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(50),
    role VARCHAR(5),
    is_active BOOLEAN
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
    con = connection_acc()
    c = con.cursor()

    c.execute("""
        INSERT INTO items (item_name, description, category, price, stock) 
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
        DROP TABLE items
        """)
    con.commit()
    con.close()
