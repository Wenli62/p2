from flask import Flask, render_template, request
from pymongo import MongoClient
import yaml
import jwt
import os

def load_yaml(file, default={}):
    try:
        with open(file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return default

app = Flask(__name__)

mongo_user = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongo_pass = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
mongo_host = os.environ.get("MONGO_HOST")
mongo_port = os.environ.get("MONGO_PORT")
mongo_db = os.environ.get("MONGO_INITDB_DATABASE")
SECRET_KEY = os.environ.get("secret_key")

mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/"

client = MongoClient(mongo_uri)
db = client[mongo_db]

stats = db["stats"]
students = db["students"]

def validate_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token, 200
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 401

@app.route("/results", methods=["GET"])
def show_results():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400
    try:
        decoded_token = validate_token(token)
    except Exception as e:
        return str(e), 401

    analytics_cursor = stats.find_one()
    if not analytics_cursor:
        return "Analytics data not found", 404

    students_cursor = students.find()
    students_data = list(students_cursor) 
    
    student_id = request.args.get("student_id", type=int)
    student = None
    if student_id:
        student = next((stu for stu in students_data if stu["student_id"] == student_id), None)
    
    return render_template("results.html", analytics=analytics_cursor, students=students_data, student=student, token=token)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5030)
