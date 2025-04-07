from flask import Flask, render_template, request, jsonify
import httpx
import logging.config
import yaml
from datetime import datetime, timezone
import jwt
import os

def load_yaml(file, default={}):
    try:
        with open(file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return default

app_config = load_yaml('app_conf.yml')
SECRET_KEY = os.environ.get("secret_key")

log_config = load_yaml('log_conf.yml')

if log_config:
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')


app = Flask(__name__)

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(payload)
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        return None

@app.route("/grade", methods=["GET", "POST"])
def submit_grade():
    
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "Missing token", 400 
        try:
            decoded_token = validate_token(token)
            return render_template('index.html', token=token)
            
        except jwt.ExpiredSignatureError:
            return "Token expired", 401
        except jwt.InvalidTokenError:
            return "Invalid token", 401

    data = request.get_json()
    required_fields = ['student_id', 'subject', 'grade']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    data["receive_time"] = datetime.now(timezone.utc).isoformat()
    logger.info(f"Grade received on {data['receive_time']}")

    url = app_config['submit_grade']['url']
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        httpx.post(url, json=data, headers=headers).raise_for_status()
        logger.info(f"Sending request to {url} with headers: {headers}")

    except Exception as e:
        logger.error(f"Error forwarding grade: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500

    return jsonify({"message": "Grade recorded successfully"}), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010)
