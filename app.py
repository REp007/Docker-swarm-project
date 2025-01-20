from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

DB_HOST = 'mysql'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'users_db'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('data.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
