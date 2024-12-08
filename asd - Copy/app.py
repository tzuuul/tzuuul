from flask import Flask, render_template, request, redirect, url_for
import bcrypt
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",   # Use localhost for local server
    user="root",        # Your MySQL username
    password="",        # Your MySQL password
    database="user_auth" # The database created earlier
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('login.html')  # Login page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into the database
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, hashed_password))
        db.commit()
        return redirect(url_for('index'))  # Redirect to login after signup
    return render_template('signup.html')  # Signup page

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Fetch user from the database
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):  # Check password
        return "Login successful!"  # Or redirect to dashboard
    else:
        return "Invalid credentials"

if __name__ == "__main__":
    app.run(debug=True)
