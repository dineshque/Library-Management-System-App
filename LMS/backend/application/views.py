from flask import current_app as app, jsonify, request, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import fields
from .security import datastore
from datetime import  datetime
from .models import db, Role

user_resource_fields = {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
}

@app.route('/user-registration', methods=['POST'])
def user_registration():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    if not (email and username and password and role_name):
        return jsonify({"message": "Incomplete data provided"}), 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"message": "Role not found"}), 404

    user = datastore.find_user(email=email)
    if user:
        return jsonify({"message": "User already registered"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    datastore.create_user(username=username,
                          email=email,
                          password=hashed_password,
                          roles=[role])
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 200

@app.route('/user-login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')
    if not (email and password and role_name):
        return jsonify({"message": "Incomplete data provided"}), 400

    user = datastore.find_user(email=email)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.last_visited = datetime.now()
    db.session.commit()
    
    user_role_names = [role.name for role in user.roles]
    if role_name not in user_role_names:
        return jsonify({"message": f"User does not have role '{role_name}'"}), 403

    if not check_password_hash(user.password, password.strip()):
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({"token": user.get_auth_token(), "username": user.username, "role": role_name}), 200
