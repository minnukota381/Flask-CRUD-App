from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.urandom(24).hex()

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)
db = client['flask-pymongo']
users_collection = db['users']

@app.route('/')
def index():
    message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/', methods=['POST'])
def insert():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        
        users_collection.insert_one({"reg_number": reg_number, "name": name})
        
        flash('Data saved successfully', 'success')
        return redirect(url_for('index', message='Data saved successfully'))

@app.route('/display')
def display():
    data = list(users_collection.find())
    return render_template('display.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        result = users_collection.find_one({"reg_number": reg_number})
        
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
        
        result = users_collection.find_one({"reg_number": reg_number})
        
        if result:
            users_collection.update_one({"reg_number": reg_number}, {"$set": {"name": name}})
            flash('Data updated successfully', 'success')
            return redirect(url_for('index', message='Data updated successfully'))
        else:
            flash('Data not found', 'error')
            return render_template('update.html', message='Data not found')
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        result = users_collection.find_one({"reg_number": reg_number})
        
        if result:
            users_collection.delete_one({"reg_number": reg_number})
            flash('Data deleted successfully', 'success')
            return render_template('delete.html', message='Data deleted successfully')
        else:
            flash('Data not found', 'error')
            return render_template('delete.html', message='Data not found')
    else:
        return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
