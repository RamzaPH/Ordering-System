from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Database connection function
def get_db_connection():
    # Construct the absolute path for the database
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'instance', 'database.db')

    # Ensure the instance directory exists
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form['firstName']
        middle_name = request.form['middleName']
        last_name = request.form['lastName']
        email = request.form['email']
        message = request.form['message']
        created_at = datetime.now()

        conn = get_db_connection()
        conn.execute('INSERT INTO contact_message (first_name, middle_name, last_name, email, message, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                     (first_name, middle_name, last_name, email, message, created_at))
        conn.commit()
        conn.close()

        flash('Message successfully submitted!', 'success')
        return redirect(url_for('success'))

    return render_template('contact.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Capture form data
        first_name = request.form['firstName']
        middle_name = request.form['middleName']
        last_name = request.form['lastName']
        name = f"{first_name} {middle_name} {last_name}"
        contact_number = request.form['contactNumber']
        street = request.form['street']
        barangay = request.form['barangay']
        city = request.form['city']
        province = request.form['province']
        quantity = request.form['quantity']
        delivery_date = request.form['deliveryDate']
        created_at = datetime.now()

        # Insert data into the database
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO "order" (name, contact_number, street_address, barangay, city_or_municipality, province, quantity, delivery_date, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (name, contact_number, street, barangay, city, province, quantity, delivery_date, created_at)
            )
            conn.commit()
            conn.close()

            flash('Order successfully placed!', 'success')
            return redirect(url_for('success'))
        except sqlite3.Error as e:
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('index'))

    return render_template('index.html')



@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/debug/<string:type>')
def debug(type):
    conn = get_db_connection()
    data = conn.execute(f'SELECT * FROM {type}').fetchall()
    conn.close()
    return render_template('debug.html', type=type, data=data)

if __name__ == '__main__':
    app.run(debug=True)
