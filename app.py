from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)   
CORS(app)               

app.secret_key = "jal_suchna_secret"


# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8265",   
    database="jal_suchna"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template("home.html")

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        village = request.form['village']
        password = request.form['password']

        sql = "INSERT INTO users (name, mobile, village, password) VALUES (%s, %s, %s, %s)"
        values = (name, mobile, village, password)
        cursor.execute(sql, values)
        db.commit()

        return "User Registered Successfully!"

    return render_template("user_register.html")
    from flask import session



@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.get_json()

    mobile = data['mobile']
    password = data['password']

    sql = "SELECT * FROM users WHERE mobile=%s AND password=%s"
    values = (mobile, password)
    cursor.execute(sql, values)
    user = cursor.fetchone()

    if user:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

#User Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template("user_dashboard.html", name=session['user'])
    else:
        return redirect('/user_login')
    
# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
        values = (username, password)
        cursor.execute(sql, values)
        admin = cursor.fetchone()

        if admin:
            session['admin'] = admin[1]
            return redirect('/admin_dashboard')
        else:
            return "Invalid Admin Credentials!"

    return render_template("admin_login.html")

#Admin Dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' in session:

        if request.method == 'POST':
            date = request.form['date']
            start = request.form['start_time']
            end = request.form['end_time']
            message = request.form['message']

            sql = "INSERT INTO water_timing (date, start_time, end_time, message) VALUES (%s,%s,%s,%s)"
            values = (date, start, end, message)
            cursor.execute(sql, values)
            db.commit()

        cursor.execute("SELECT * FROM water_timing ORDER BY date DESC")
        timings = cursor.fetchall()

        return render_template("admin_dashboard.html", timings=timings)

    return redirect('/admin_login')
#Delete Timing 
@app.route('/delete_timing/<int:id>')
def delete_timing(id):
    if 'admin' in session:
        sql = "DELETE FROM water_timing WHERE id=%s"
        cursor.execute(sql, (id,))
        db.commit()
        return redirect('/admin_dashboard')
    return redirect('/admin_login')


if __name__ == '__main__':
    app.run(debug=True)
