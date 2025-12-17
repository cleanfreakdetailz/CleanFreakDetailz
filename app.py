from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cleanfreakdetailz@4600'  # Change this to a secure random key

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'cleanfreakdetailz@gmail.com'
EMAIL_PASSWORD = 'aolp blof tuee ireq'

# =========================
# Google Site Verification
# =========================
@app.route('/google89aa697c5ee6a684.html')
def google_verify():
    return send_from_directory('static', 'google89aa697c5ee6a684.html')


@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/contact')
def contact():
    return render_template('contactme.html')


@app.route('/services')
def services():
    return render_template('services.html', title='Our Services')


@app.route('/extraservices')
def extraservices():
    return render_template('extraservices.html', title='Extra Services')


@app.route('/packages')
def packages():
    return render_template('packages.html', title='Service Packages')


@app.route('/cart')
def cart():
    return render_template('cart.html', title='Your Cart')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html', title='Checkout')


@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    item = {
        'id': data.get('id'),
        'name': data.get('name'),
        'price': data.get('price'),
        'type': data.get('type'),
        'image': data.get('image', '')
    }

    cart = session.get('cart', [])
    if not any(c['id'] == item['id'] and c['type'] == item['type'] for c in cart):
        cart.append(item)
        session['cart'] = cart

    return jsonify({'success': True, 'cart_count': len(cart)})


@app.route('/api/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    cart = session.get('cart', [])
    session['cart'] = [
        item for item in cart
        if not (item['id'] == data.get('id') and item['type'] == data.get('type'))
    ]
    return jsonify({'success': True, 'cart_count': len(session['cart'])})


@app.route('/api/get-cart')
def get_cart():
    return jsonify(session.get('cart', []))


@app.route('/api/submit-order', methods=['POST'])
def submit_order():
    try:
        data = request.json
        cart_items = data.get('cart', [])
        customer_info = data.get('customer_info', {})

        subject = f"New Order from {customer_info.get('name', 'Customer')}"

        message = f"""
Customer Information:
Name: {customer_info.get('name')}
Email: {customer_info.get('email')}
Phone: {customer_info.get('phone')}
Address: {customer_info.get('address')}
Preferred Date: {customer_info.get('date')}
Vehicle Info: {customer_info.get('vehicle')}
Additional Info: {customer_info.get('additional_info')}

Order Items:
"""
        total = 0
        for item in cart_items:
            message += f"- {item['name']}: ${item['price']}\n"
            total += float(item['price'])

        message += f"\nTotal: ${total:.2f}"
        message += f"\nReceived at: {datetime.now()}"

        send_email(EMAIL_USER, subject, message)
        session['cart'] = []

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, to_email, msg.as_string())
    server.quit()


if __name__ == '__main__':
    app.run(debug=True)
