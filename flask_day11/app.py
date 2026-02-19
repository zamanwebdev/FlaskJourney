from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask API Running"

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()

    name = data.get('name')
    age = data.get('age')
    country = data.get('country')

    response = {
        "message": "User created successfully!",
        "user": {
            "name": name,
            "age": age,
            "country": country
        }
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
