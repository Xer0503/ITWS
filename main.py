from flask import Flask, render_template, request, url_for, redirect, session
from connection import connection_prod, connection_acc, connection_order
from db import query_items, query_feedback
from customer_query import customer_query, active_customer
from products_query import query_items, query_feedback

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
@app.route('/home')
def home():
    return render_template('frontPage.html')

@app.route('/shop')
def shop():
    data = query_items()
    if 'role' in session and session['role'] == 'user':
        return render_template('shopPage.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/devs')
def aboutUs():
    return render_template('developer_user_side.html')

@app.route('/admin/devs')
def developer():
    return render_template('/admin/developers.html')

@app.route('/admin')
def admin():
    total_customers = customer_query()
    total_active_customers = active_customer()
    total_items = query_items()
    total_feedback = query_feedback()
    if 'role' in session and session['role'] == 'admin':
        return render_template('/admin/index.html', 
                               total_customers = total_customers, 
                               total_active_customers = total_active_customers,
                               total_items = total_items,
                               total_feedback = total_feedback
                               )
    else:
        return redirect(url_for('home'))  # or 403 error if preferred


@app.route('/admin/customer_table')
def customer_table():
    customer = customer_query()
    return render_template('/admin/tables_accounts.html', customer = customer)

@app.route('/admin/customer_table', methods = ['POST', 'GET'])
def manage_customer():
    if request.method == 'POST':
        if 'customer_id' in request.form:  # Handle delete
            customer_id = request.form['customer_id']
            delete_customer_sql(customer_id)
        elif 'customer_edit_id' in request.form:  # Handle update
            customer_edit_info = (
                request.form['first_name'],
                request.form['last_name'],
                request.form['phone'],
                request.form['address'],
                request.form['email'],
                request.form['password'],
                request.form['role'],
                1 if request.form['status'] == 'active' else 0,
                request.form['customer_edit_id']
            )
            update_customer_sql(customer_edit_info)
        return redirect(url_for('customer_table'))
    
    return redirect(url_for('customer_table'))

def delete_customer_sql(customer_id):
    con = connection_acc()
    c = con.cursor()

    sql = 'DELETE FROM customer WHERE customer_id=?'
    c.execute(sql, (customer_id,))

    con.commit()
    con.close()

@app.route('/admin/customer_table', methods = ['POST', 'GET'])
def update_customer():
    if request.method == 'POST':
        customer_edit_info = (
        request.form['first_name'],
        request.form['last_name'],
        request.form['phone'],
        request.form['address'],
        request.form['email'],
        request.form['password'],
        request.form['role'],
        1 if request.form['status'] == 'active' else 0,
        request.form['customer_edit_id']
        )

        update_customer_sql(customer_edit_info)
        return redirect(url_for('customer_table'))
    
    return redirect(url_for('customer_table'))

def update_customer_sql(customer_edit_info):
    con = connection_acc()
    c = con.cursor()

    sql = '''UPDATE customer 
         SET first_name = ?, last_name = ?, phone = ?, address = ?, email = ?, password = ?, role = ?, is_active = ?  
         WHERE customer_id = ?'''

    c.execute(sql, customer_edit_info)

    con.commit()
    con.close()

@app.route('/admin/products')
def products_table():
    items = query_items()
    return render_template('/admin/tables_products.html', items = items)

@app.route('/admin/products', methods = ['POST'])
def manage_products():
    if request.method == 'POST':
        if 'product_id' in request.form:  # Handle delete
            product_id = request.form['product_id']
            delete_product_sql(product_id)
        elif 'product_edit_id' in request.form:  # Handle update
            product_edit_info = (
            request.form['name'],
            request.form['description'],
            request.form['price'],
            request.form['stocks'],
            request.form['category'],
            request.form['product_edit_id']
            )
            update_product_sql(product_edit_info)
        return redirect(url_for('products_table'))
    
    return redirect(url_for('products_table'))

@app.route('/admin/add_products', methods = ['POST'])
def add_products():
    if request.method == 'POST':
        itemsInput = (
            request.form['name'],
            request.form['description'],
            request.form['price'],
            request.form['stocks'],
            request.form['category']
        )
        sql_addItem(itemsInput)
        return redirect(url_for('products_table'))
    
    return redirect(url_for('products_table'))


def sql_addItem(itemsInput):
    con = connection_prod()
    c = con.cursor()

    sql = 'INSERT INTO items (item_name, item_description, item_price, item_stock, item_category) VALUES (?,?,?,?,?)'

    c.execute(sql, itemsInput)
    con.commit()
    con.close()

def delete_product_sql(product_id): #delete product
    con = connection_prod()
    c = con.cursor()

    sql = 'DELETE FROM items WHERE item_id=?'
    c.execute(sql, (product_id,))

    con.commit()
    con.close()

def update_product_sql(product_edit_info):
    con = connection_prod()
    c = con.cursor()

    sql = '''UPDATE items SET item_name = ?, item_description = ?, item_price = ?, item_stock = ?, item_category = ? WHERE item_id = ?'''
    
    c.execute(sql, product_edit_info)

    con.commit()
    con.close()

@app.route('/feedback', methods = ['POST'])
def feedback():
    if request.method == 'POST':
        comment = (
            request.form['name'],
            request.form['description']
        )
        addFeedback(comment)
        return render_template('frontPage.html', msg = 'Thanks for your feedback!')
    return home()

def addFeedback(comment):
    con = connection_prod()
    c = con.cursor()

    sql = 'INSERT INTO feedback (name, description) VALUES (?, ?)'

    c.execute(sql, comment)
    con.commit()
    con.close()

@app.route('/admin/feedback')
def feedback_table():
    comments = query_feedback()
    return render_template('/admin/tables_feedback.html', comments = comments)

@app.route('/admin/feedback', methods = ['POST'])
def delete_feedback():
    if request.method == 'POST':
        feedback_id = request.form['feedback_id']
        delete_feedback_sql(feedback_id)
        return redirect(url_for('feedback_table'))
    
    return redirect(url_for('feedback_table'))

def delete_feedback_sql(feedback_id):
    con = connection_prod()
    c = con.cursor()

    sql = 'DELETE FROM feedback WHERE id=?'
    c.execute(sql, (feedback_id,))

    con.commit()
    con.close()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_validation():
    con = connection_acc()
    cursor = con.cursor()
    email = request.form['email']
    password = request.form['password']

    try:
        cursor.execute("SELECT * FROM customer WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if not user:
            cursor.execute("SELECT * FROM admin WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
            session['first_name'] = user[1]
            session['last_name'] = user[2]
            session['email'] = user[3]  

        if user:
            session['user_id'] = user[0]
            session['first_name'] = user[1]
            session['last_name'] = user[2]
            session['phone'] = user[3]
            session['address'] = user[4]
            session['email'] = user[5]


            user_id = session.get('user_id')
            cursor.execute("UPDATE customer SET is_active = 1 WHERE customer_id = ?", (user_id,))
            con.commit()
            con.close()

            if len(user) > 7: 
                session['role'] = user[7] 
            else:
                session['role'] = user[5]

            # Redirect based on role
            if session['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('shop'))

        else:
            return render_template('login.html', wrong='Invalid email or password')
        
    except Exception as e:
        print("Error during login:", e)
        return render_template('login.html', wrong='Invalid email or password')

def validate(acc_validate):    
    con = connection_acc()
    c = con.cursor()
    sql = 'SELECT * FROM customer WHERE email=? AND password=?'
    c.execute(sql, acc_validate)
    
    verify = c.fetchall()
    con.commit()
    con.close()

    return verify

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_validation():
    if request.method == 'POST':
        user_acc = (
            request.form['first_name'],
            request.form['last_name'],
            request.form['contacts'],
            request.form['address'],
            request.form['email'],
            request.form['password'],
            'user',
            True
        )
        signup_add(user_acc)
        return redirect(url_for('login'))
    
    return redirect(url_for('signup'))
    
def signup_add(user_acc):
    con = connection_acc()
    c = con.cursor()

    sql = 'INSERT INTO customer(first_name, last_name, phone, address, email, password, role, is_active) VALUES (?,?,?,?,?,?,?,?)'
    c.execute(sql, user_acc)

    con.commit()
    con.close()

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    con = connection_acc()
    cursor = con.cursor()
    user_id = session.get('user_id')
    role = session.get('role')

    # Mark user as inactive in the DB
    if role == 'user':
        cursor.execute("UPDATE customer SET is_active = 0 WHERE customer_id = ?", (user_id,))
    
    con.commit()
    session.clear()
    return redirect(url_for('login'))

@app.route('/buy_items', methods=['POST'])
def buy_items():
    customer_id = session['user_id']
    item_id = request.form['item_id']
    item_price = request.form['item_price']
    quantity = request.form['quantity']
    total_price = float(item_price) * float(quantity)
    add_order(customer_id, item_id, quantity, total_price)

    return redirect(url_for('shop'))

def add_order(customer_id, item_id, quantity, total_price):
    con = connection_order()
    c = con.cursor()

    sql = 'INSERT INTO order_details (customer_id, item_id, order_quantity, order_price) VALUES (?, ?, ?, ?)'
    c.execute(sql, (customer_id, item_id, quantity, total_price))

    con.commit()
    con.close()

    return redirect(url_for('shop'))

@app.route('/view/order')
def view_order():
    orders = view_order_customer()
    return render_template('view_order.html', orders=orders)

def view_order_customer():
    con = connection_order()
    c = con.cursor()

    sql = 'SELECT * FROM order_details WHERE customer_id=?'
    c.execute(sql, (session['user_id'],))
    orders = c.fetchall()
    con.commit()
    con.close()

    return orders

def fetch_item_details():
    item_detail = view_order_customer()
    item_id = item_detail
    con = connection_prod()
    c = con.cursor()

    sql = 'SELECT * FROM items'
    c.execute(sql)
    items = c.fetchall()
    con.commit()
    con.close()

    return items

if __name__ == '__main__':
    app.run(debug=True)