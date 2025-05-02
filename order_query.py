from connection import connection_order, connection_prod, connection_acc

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

    return data