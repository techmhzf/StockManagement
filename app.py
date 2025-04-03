from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
from database import db  # ✅ Corrected import
from database.models import User, Stock  # ✅ Ensure these models exist

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Initialize Extensions
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect('/register')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    stocks = Stock.query.all()
    return render_template('dashboard.html', name=current_user.name, stocks=stocks)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect('/login')

@app.route('/api/stocks')
def stock_data():
    stocks = Stock.query.all()
    data = [{"symbol": stock.symbol, "company": stock.company, "price": stock.price, "change": stock.change} for stock in stocks]
    return jsonify(data)

# Create Database Tables
with app.app_context():
    db.create_all()  # ✅ This ensures database tables are created

if __name__ == '__main__':
    app.run(debug=True)