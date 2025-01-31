from flask import Flask, request, render_template
import pymysql
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP Request Latency', ['endpoint'])

# Database configuration
DB_HOST = 'mysql'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'users_db'

@app.before_request
def before_request():
    # Count each request by method and endpoint
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.after_request
def after_request(response):
    # Placeholder for request latency (adjust later if needed)
    # Since Flask doesn't track request time directly, this is omitted
    return response

@app.route('/metrics')
def metrics():
    # Expose metrics for Prometheus
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/test')
def test():
    # Simple test route
    return 'Hello Test'

@app.route('/')
def form():
    # Render the form.html template
    return render_template('form.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    # Connect to MySQL
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Insert data into the database
        name = request.form['name']
        email = request.form['email']
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()

    # Fetch all data from the users table
    cursor.execute("SELECT name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('data.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
