from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Initialize Flask App
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/"  # Use local MongoDB or Atlas URI
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize MongoDB and Extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.password = user_data["password"]

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        user_exists = mongo.db.users.find_one({"email": email})
        if user_exists:
            flash("Email already registered!", "danger")
            return redirect('/register')

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        flash("Registration successful! Please login.", "success")
        return redirect('/login')

    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_data = mongo.db.users.find_one({"email": email})
        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            flash("Login successful!", "success")
            return redirect('/dashboard')

        flash("Invalid credentials!", "danger")

    return render_template('login.html')

# User Dashboard (Protected Route)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

# Fetch Stock Price API
@app.route('/api/stocks/<symbol>')
def stock_price(symbol):
    from api.api import get_stock_price  # Import function from api/api.py
    price = get_stock_price(symbol)
    return jsonify({"symbol": symbol, "price": price})

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect('/login')

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)