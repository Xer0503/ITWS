from flask import Flask, render_template, request, url_for, redirect, session, Response
from connection import connection_prod, connection_acc, connection_order, connection_cart
from db import query_items, query_feedback
from customer_query import customer_query, active_customer
from products_query import query_items, query_feedback
from query_order import query_order

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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

#Admin Section
@app.route('/admin/devs')
def developer():
    return render_template('/admin/developers.html')

#admin rendering data sa dashboard
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
        return redirect(url_for('home'))
#end dashboard

#admin managing customer accounts
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
        file = request.files.get('file_img')
        image = file.read()
        itemsInput = (
            request.form['name'],
            request.form['description'],
            request.form['price'],
            request.form['stocks'],
            request.form['category'],
            image
        )
        sql_addItem(itemsInput)
        return redirect(url_for('products_table'))
    
    return redirect(url_for('products_table'))


def sql_addItem(itemsInput):
    con = connection_prod()
    c = con.cursor()

    sql = 'INSERT INTO items (item_name, item_description, item_price, item_stock, item_category, item_image) VALUES (?,?,?,?,?,?)'

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

@app.route('/image/<int:item_id>')
def get_image(item_id):
    con = connection_prod()
    c = con.cursor()
    c.execute("SELECT item_image FROM items WHERE item_id = ?", (item_id,))
    row = c.fetchone()
    con.close()

    if row and row[0]:
        return Response(row[0], mimetype="image/jpeg")
    return '', 404


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

#for authentication code
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('shop'))
    elif 'role' in session and session['role'] == 'admin':
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_validation():
    con = connection_acc()
    c = con.cursor()
    email = request.form['email']
    password = request.form['password']

    if email and password:
        c.execute("SELECT * FROM customer WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        role = 'user'

        if not user:
            c.execute("SELECT * FROM admin WHERE email = ? AND password = ?", (email, password))
            user = c.fetchone()
            role = 'admin' if user else None

        if user:
            session['user_id'] = user[0]
            session['first_name'] = user[1]
            session['last_name'] = user[2]
            session['email'] = user[5]

            if role == 'user':
                session['phone'] = user[3]
                session['address'] = user[4]
                session['role'] = user[7] if len(user) > 7 else 'user'
                c.execute("UPDATE customer SET is_active = 1 WHERE customer_id = ?", (user[0],))
                con.commit()
                con.close()

                return redirect(url_for('shop'))

            elif role == 'admin':
                session['role'] = 'admin'
                con.close()
                return redirect(url_for('admin'))

        else:
            con.close()
            return render_template('login.html', wrong='Account not Found (Sign up first), or Enter Correct Email or Password')
    else:
        return render_template('login.html', wrong='Wrong Email or Password')

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

    if role == 'user':
        cursor.execute("UPDATE customer SET is_active = 0 WHERE customer_id = ?", (user_id,))
    
    con.commit()
    session.clear()
    return redirect(url_for('login'))
# end of authentication code

# for order and cart code
@app.route('/buy_items/cart', methods=['POST'])
def buy_items_fr_cart():
    cart_id = request.form['cart_id']

    if cart_id:
        con = connection_cart()
        c = con.cursor()
        sql = 'SELECT * FROM cart WHERE cart_id=?'
        c.execute(sql, (cart_id,))
        cart = c.fetchone()
        con.commit()
        con.close()

        if cart:
            print('cart: ', cart)
            customer_id = cart[1]
            item_id = cart[2]
            item_name = cart[3]
            quantity = cart[4]
            item_price = cart[5]
            item_category = cart[6]
            total_price = float(item_price) * float(quantity)
            add_order(customer_id, item_id, quantity, total_price, item_name, item_category)
            delete_cart_sql(cart_id)  # Delete naman after buying

            return redirect(url_for('view_cart'))
        
    return redirect(url_for('view_cart'))

@app.route('/buy_items', methods=['POST'])
def buy_items():
    #in buy 
    con = connection_prod()
    c = con.cursor()
    
    customer_id = session['user_id']
    item_id = request.form['item_id']
    item_name = request.form['item_name']
    item_category = request.form['item_category']
    item_price = request.form['item_price']
    quantity = request.form['quantity']
    total_price = float(item_price) * float(quantity)

    add_order(customer_id, item_id, quantity, total_price, item_name, item_category)

    return redirect(url_for('shop'))
    

def add_order(customer_id, item_id, quantity, total_price, item_name, item_category):
    con = connection_order()
    c = con.cursor()

    sql = 'INSERT INTO order_details (customer_id, item_id, order_quantity, order_price, order_item, order_category) VALUES (?, ?, ?, ?, ?, ?)'
    c.execute(sql, (customer_id, item_id, quantity, total_price, item_name, item_category))

    con.commit()
    con.close()

    return redirect(url_for('shop'))

@app.route('/view/order')
def view_order():
    orders = view_order_customer()
    return render_template('view_order.html', orders=orders)

def view_order_customer():
    if 'user_id' not in session:
        return []

    con = connection_order()
    c = con.cursor()

    sql = 'SELECT * FROM order_details WHERE customer_id=?'
    c.execute(sql, (session['user_id'],))
    orders = c.fetchall()
    con.close()

    return orders

@app.route('/delete_order', methods=['POST', 'GET'])
def cancel_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        delete_order_sql(order_id)
        return redirect(url_for('view_order'))

@app.route('/delete_cart', methods=['POST', 'GET'])
def cancel_cart():
    if request.method == 'POST':
        cart_id = request.form['cart_id']
        delete_cart_sql(cart_id)
        return redirect(url_for('view_cart'))

def delete_order_sql(order_id):
    con = connection_order()
    c = con.cursor()

    sql = 'DELETE FROM order_details WHERE order_id=?'
    c.execute(sql, (order_id,))

    con.commit()
    con.close()

def delete_cart_sql(cart_id):
    con = connection_order()
    c = con.cursor()

    sql = 'DELETE FROM cart WHERE cart_id=?'
    c.execute(sql, (cart_id,))

    con.commit()
    con.close()

@app.route('/cart_items', methods=['POST'])
def cart_items():
    customer_id = session['user_id']
    item_id = request.form['item_id']
    item_name = request.form['item_name']
    item_category = request.form['item_category']
    item_price = request.form['item_price']
    quantity = request.form['quantity']
    total_price = float(item_price) * float(quantity)
    cart_order(customer_id, item_id, quantity, total_price, item_name, item_category)

    return redirect(url_for('shop'))

def cart_order(customer_id, item_id, quantity, total_price, item_name, item_category):
    con = connection_order()
    c = con.cursor()

    sql = 'INSERT INTO cart (customer_id, product_id, item_name, item_quantity, item_price, item_category) VALUES (?, ?, ?, ?, ?, ?)'
    c.execute(sql, (customer_id, item_id, item_name, quantity, total_price, item_category))

    con.commit()
    con.close()

    return redirect(url_for('shop'))

@app.route('/view/cart')
def view_cart():
    cart = view_cart_customer()
    return render_template('view_cart.html', cart=cart)

def view_cart_customer():
    if 'user_id' not in session:
        return []

    con = connection_order()
    c = con.cursor()

    sql = 'SELECT * FROM cart WHERE customer_id=?'
    c.execute(sql, (session['user_id'],))
    cart = c.fetchall()
    con.close()
    
    return cart
# end of order and cart code

# for admin view transaction record code
@app.route('/admin/view_transaction')
def view_transaction():
    transaction = query_order()
    return render_template('/admin/transaction_order.html', transaction=transaction)

@app.route('/admin/delete_transaction', methods=['POST', 'GET'])
def delete_transaction():
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        delete_transaction_sql(transaction_id)
        return redirect(url_for('view_transaction'))
    
def delete_transaction_sql(transaction_id):
    con = connection_order()
    c = con.cursor()

    sql = 'DELETE FROM order_details WHERE order_id=?'
    c.execute(sql, (transaction_id,))

    con.commit()
    con.close()

@app.route('/admin/view_expand', methods = ['POST'])
def expand_view_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        product_id = request.form['item_id']
        customer_details = query_customer_info(customer_id)
        item_details = query_items_info(product_id)

        return render_template('/admin/expand_view_order.html', customer_details=customer_details, item_details=item_details)


def query_customer_info(customer_id):
    con = connection_acc()
    c = con.cursor()

    sql = 'SELECT * FROM customer WHERE customer_id=?'
    c.execute(sql, (customer_id,))
    customer_details = c.fetchone()
    con.commit()
    con.close()

    return customer_details

def query_items_info(item_id):
    con = connection_prod()
    c = con.cursor()

    sql = 'SELECT * FROM items WHERE item_id=?'
    c.execute(sql, (item_id,))
    item_details = c.fetchone()
    con.commit()
    con.close()

    for item in item_details:
        print(item)

    return item_details
# end view transaction record code

if __name__ == '__main__':
    app.run(debug=True)