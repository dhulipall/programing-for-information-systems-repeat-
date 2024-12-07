from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with authentication."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # For simplicity, using hardcoded credentials
        if username == 'admin' and password == 'password':
            return redirect(url_for('inventory.inventory'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')
