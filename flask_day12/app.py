from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake database (dictionary)
users = {}

@app.route('/')
def home():
    return "CRUD API Running"

# CREATE
@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = data.get('id')
    name = data.get('name')

    if not user_id or not name:
        return jsonify({"error": "ID and Name required"}), 400

    users[user_id] = {"name": name}
    return jsonify({"message": "User created", "users": users}), 201

# READ
@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify(users[user_id])

# UPDATE
@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get('name')

    users[user_id]['name'] = name
    return jsonify({"message": "User updated", "user": users[user_id]})

# DELETE
@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)
