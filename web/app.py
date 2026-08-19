import os
from flask import Flask, jsonify, render_template
import redis

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/count")
def get_count():
    count = int(r.get("hits") or 0)
    return jsonify({"count": count})


@app.route("/api/hit", methods=["POST"])
def hit():
    count = r.incr("hits")
    return jsonify({"count": count})


@app.route("/api/reset", methods=["POST"])
def reset():
    r.set("hits", 0)
    return jsonify({"count": 0})


@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "ok", "redis": "connected"}), 200
    except redis.exceptions.ConnectionError:
        return jsonify({"status": "error", "redis": "unreachable"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
