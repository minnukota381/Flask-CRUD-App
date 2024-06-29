# DATABASE_URL=postgresql://postgres:12345@localhost:5432/my_flask_db


from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')

def create_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_database_and_table():
    admin_conn_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '12345',
        'host': 'localhost',
        'port': '5432'
    }

    db_name = 'my_flask_db'
    table_name = 'users'

    try:
        admin_conn = psycopg2.connect(**admin_conn_params)
        admin_conn.autocommit = True
        admin_cursor = admin_conn.cursor()
        admin_cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
        exists = admin_cursor.fetchone()
        if not exists:
            admin_cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully")
        else:
            print(f"Database '{db_name}' already exists")
        admin_cursor.close()
        admin_conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                reg_number VARCHAR(100) NOT NULL,
                name VARCHAR(100) NOT NULL
            )
        ''')
        conn.commit()
        print(f"Table '{table_name}' created successfully")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

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
    create_database_and_table()
    app.run(debug=True, host='0.0.0.0')
