from connection import connection_order

def query_order():
    con = connection_order()
    c = con.cursor()

    c.execute("""
    SELECT * FROM order_details
    """
    )

    data = c.fetchall()
    con.commit()
    con.close()
    for i in data:
        print('fetch order: ', i)

    return data
