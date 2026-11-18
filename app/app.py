import time
import random
import logging
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("observability-app")

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds', ['endpoint'])

@app.route('/')
def hello():
    start_time = time.time()
    latency = random.uniform(0.05, 0.3)
    time.sleep(latency)
    
    # 15% error rate simulate karte hain taaki Grafana mein spikes dikhein
    status = 200
    if random.random() < 0.15:
        status = 500
        logger.error("Internal Server Error simulated!")
    else:
        logger.info("Successfully handled request to /")

    REQUEST_COUNT.labels(method='GET', endpoint='/', status=str(status)).inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(latency)
    
    if status == 500:
        return "Internal Server Error", 500
    return "Hello from Upgraded Observability Suite!", 200

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)