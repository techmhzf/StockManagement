from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import yfinance as yf

# Flask App Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database & Encryption Setup
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Fetch Live Stock Data
def fetch_stock_data():
    symbols = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']
    stock_data = []

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        info = stock.info
        stock_data.append({
            'symbol': symbol,
            'name': info.get('shortName', 'N/A'),
            'price': round(info.get('regularMarketPrice', 0), 2),
            'change': round(info.get('regularMarketChangePercent', 0), 2)
        })

    return stock_data

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Registration Route
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

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    stock_data = fetch_stock_data()
    return render_template('dashboard.html', name=current_user.name, stocks=stock_data)

# Portfolio Route
@app.route('/portfolio')
@login_required
def portfolio():
    stock_data = fetch_stock_data()
    return render_template('portfolio.html', name=current_user.name, stocks=stock_data)

# Profile Route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, email=current_user.email)

# API Route for Live Stock Data
@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    return jsonify(fetch_stock_data())

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect('/')

# Run the Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)