from connection import connection_prod

def query_items():
    con = connection_prod()

    c = con.cursor()

    c.execute("""
    SELECT * FROM items
    """
    )

    items = c.fetchall()
    con.commit()
    con.close()

    return items

def query_feedback():
    con = connection_prod()

    c = con.cursor()

    c.execute("""
    SELECT * FROM feedback
    """
    )

    feedback = c.fetchall()
    con.commit()
    con.close()

    return feedback