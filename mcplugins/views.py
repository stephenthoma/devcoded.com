from mcplugins import app
from flask import render_template
#from flask.ext.login import login_required, current_user

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("sign_up.html")

@app.route('/dashboard')
#@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/order')
def order():
    return render_template("order.html")
