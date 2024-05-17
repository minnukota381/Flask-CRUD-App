from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

def create_connection():
    conn = pymysql.connect(
        host='localhost',
        user=os.getenv('MYSQL_USERNAME'),
        password=os.getenv('MYSQL_PASSWORD'),
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS flask_mysql")
        conn.commit()

    conn = pymysql.connect(
        host='localhost',
        user=os.getenv('MYSQL_USERNAME'),
        password=os.getenv('MYSQL_PASSWORD'),
        database='flask_mysql',
        cursorclass=pymysql.cursors.DictCursor
    )

    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reg_number VARCHAR(255),
                    name VARCHAR(255))''')
    conn.commit()

@app.route('/')
def index():
    message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/', methods=['POST'])
def insert():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (reg_number, name) VALUES (%s, %s)", (reg_number, name))
        conn.commit()
        conn.close()
        
        flash('Data saved successfully', 'success')
        return redirect(url_for('index', message='Data saved successfully'))

@app.route('/display')
def display():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    
    return render_template('display.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE reg_number=%s", (reg_number,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return render_template('display.html', data=[result])
        else:
            return render_template('search.html', message='Data not found', reg_number=reg_number)
    else:
        return render_template('search.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name=%s WHERE reg_number=%s", (name, reg_number))
        conn.commit()
        conn.close()
        
        flash('Data updated successfully', 'success')
        return redirect(url_for('index', message='Data updated successfully'))
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE reg_number=%s", (reg_number,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("DELETE FROM users WHERE reg_number=%s", (reg_number,))
            conn.commit()
            conn.close()
            flash('Data deleted successfully', 'success')
            return render_template('delete.html', message='Data deleted successfully')
        else:
            conn.close()
            flash('Data not found', 'error')
            return render_template('delete.html', message='Data not found')
    else:
        return render_template('delete.html')

if __name__ == '__main__':
    create_table(create_connection()) 
    app.run(debug=True)
