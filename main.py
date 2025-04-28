from flask import Flask, render_template, request, url_for, redirect
from connection import connection_prod, connection_acc
from db import query_items, query_feedback

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('frontPage.html')

@app.route('/shop')
def shop():
    data = query_items()
    msgs = request.args.get('msgs')
    return render_template('shopPage.html', data = data, msgs = msgs)

@app.route('/devs')
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/add', methods = ['POST'])
def addProducts():
    if request.method == 'POST':
        itemsInput = (
            request.form['name'],
            request.form['description'],
            request.form['price'],
            request.form['stocks'],
            request.form['category']
        )
        sql_addItem(itemsInput)
        return redirect(url_for('shop', msgs = 'successful added!'))
    
    return redirect(url_for('shop'))

def sql_addItem(itemsInput):
    con = connection_prod()
    c = con.cursor()

    sql = 'INSERT INTO items (item_name, description, price, stock, category) VALUES (?,?,?,?,?)'

    c.execute(sql, itemsInput)
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

@app.route('/showFeedback')
def feedbackSection():
    comments = query_feedback()
    return render_template('feedback.html', comments = comments)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login_validation():
    acc_validate = (
        request.form['email'],
        request.form['password']
    )
    verify = validate(acc_validate)

    if len(verify) > 0:
        return redirect(url_for('shop'))
    else:
        return render_template('login.html', wrong = 'Wrong Email or Password')

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

    sql = 'INSERT INTO customer(first_name, last_name, contacts, address, email, password, role, is_active) VALUES (?,?,?,?,?,?,?,?)'
    c.execute(sql, user_acc)

    con.commit()
    con.close()


if __name__ == '__main__':
    app.run(debug=True)