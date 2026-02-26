from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation import generate_plan

app = Flask(_name_)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    result = generate_plan(data)
    return jsonify(result)

if _name_ == "_main_":
    app.run(debug=True)
