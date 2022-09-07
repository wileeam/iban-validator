from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello there!"


@app.route("/validate", methods=["GET", "POST"])
def validate():
    return "Nothing"
