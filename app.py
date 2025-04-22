from flask import Flask, jsonify, request
import random
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

BROKER_URL = "http://127.0.0.1:5000"

# Register the service
def register_service():
    data = {
        "service_name": "randomNumberGenerator",
        "service_ip": "127.0.0.1",
        "service_port":"5001",
    }
    requests.post(f"{BROKER_URL}/add_service", json=data)

# Deregister the service
def deregister_service():
    data = {"service_name": "randomNumberGenerator"}
    requests.post(f"{BROKER_URL}/remove_service", json=data)

@app.route("/info", methods=["GET"])
def info():
    return jsonify({"service_name": "randomNumberGenerator"})


# Random number generator with user-defined limits
@app.route("/random", methods=["POST"])
def generate_random():
    data = request.json
    min_value = data.get("min_value", 1)
    max_value = data.get("max_value", 100)

    # Validate input
    if not isinstance(min_value, int) or not isinstance(max_value, int):
        return jsonify({"success": False, "message": "min_value and max_value must be integers"}), 400
    if min_value >= max_value:
        return jsonify({"success": False, "message": "min_value must be less than max_value"}), 400

    random_number = random.randint(min_value, max_value)
    return jsonify({"success": True, "random_number": random_number})

if __name__ == "__main__":
    register_service()
    app.run(port=5001, debug=True)
