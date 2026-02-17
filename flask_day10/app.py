from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Flask API"

@app.route('/api')
def api():
    data = {
        "name": "Zaman",
        "role": "Backend Developer",
        "skill": "Flask"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
