from flask import Flask, render_template
import os

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)