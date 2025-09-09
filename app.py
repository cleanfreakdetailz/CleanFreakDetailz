from flask import Flask, render_template, request, jsonify, session
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cleanfreakdetailz@4600'  # Change this to a secure random key

# Email configuration (update with your email details)
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USER = 'cleanfreakdetailz@gmail.com'  # Your email address
EMAIL_PASSWORD = 'aolp blof tuee ireq'  # Your email password or app-specific password

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


# New routes for cart functionality
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

    # Get or initialize cart
    cart = session.get('cart', [])

    # Check if item already exists in cart
    item_exists = False
    for cart_item in cart:
        if cart_item['id'] == item['id'] and cart_item['type'] == item['type']:
            item_exists = True
            break

    if not item_exists:
        cart.append(item)
        session['cart'] = cart

    return jsonify({'success': True, 'cart_count': len(cart)})


@app.route('/api/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    item_id = data.get('id')
    item_type = data.get('type')

    cart = session.get('cart', [])

    # Remove the item
    cart = [item for item in cart if not (item['id'] == item_id and item['type'] == item_type)]

    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': len(cart)})


@app.route('/api/get-cart')
def get_cart():
    cart = session.get('cart', [])
    return jsonify(cart)


@app.route('/api/submit-order', methods=['POST'])
def submit_order():
    try:
        data = request.json
        cart_items = data.get('cart', [])
        customer_info = data.get('customer_info', {})

        # Create email message
        subject = f"New Order from {customer_info.get('name', 'Customer')}"

        # Build email body
        message = f"""
        New Order Details:

        Customer Information:
        Name: {customer_info.get('name', 'Not provided')}
        Email: {customer_info.get('email', 'Not provided')}
        Phone: {customer_info.get('phone', 'Not provided')}
        Address: {customer_info.get('address', 'Not provided')}
        Preferred Date: {customer_info.get('date', 'Not specified')}
        Vehicle Info: {customer_info.get('vehicle', 'Not provided')}
        Additional Info: {customer_info.get('additional_info', 'None')}

        Order Items:
        """

        total = 0
        for item in cart_items:
            message += f"- {item['name']}: ${item['price']}\n"
            total += float(item['price'])

        message += f"\nTotal: ${total:.2f}"
        message += f"\n\nOrder received at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Send email
        send_email(EMAIL_USER, subject, message)

        # Clear the cart after successful order
        session['cart'] = []

        return jsonify({'success': True, 'message': 'Order submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


if __name__ == '__main__':
    app.run(debug=True)