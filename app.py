from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password' 

db = SQLAlchemy(app)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    barangay = db.Column(db.String(100), nullable=False)
    city_or_municipality = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        email = request.form['email']
        message = request.form['message']

        contact = ContactMessage(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            message=message
        )
        db.session.add(contact)
        db.session.commit()
        flash('Message submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('index'))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    try:
        name = request.form['name']
        contact_number = request.form['contact_number']
        street_address = request.form['street_address']
        barangay = request.form['barangay']
        city_or_municipality = request.form['city_or_municipality']
        province = request.form['province']
        quantity = int(request.form['quantity'])
        delivery_date = datetime.strptime(request.form['delivery_date'], '%Y-%m-%d')

        order = Order(
            name=name,
            contact_number=contact_number,
            street_address=street_address,
            barangay=barangay,
            city_or_municipality=city_or_municipality,
            province=province,
            quantity=quantity,
            delivery_date=delivery_date
        )
        db.session.add(order)
        db.session.commit()
        flash('Order submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)