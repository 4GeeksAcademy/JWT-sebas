from flask import request, jsonify, Blueprint
from api.models import db, User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

api = Blueprint('api', __name__)

# ----------- SIGNUP -----------
@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "email y password son requeridos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "email ya existe"}), 409

    user = User(email=email)
    user.set_password(password)       # asegúrate que User tiene este método
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "usuario creado"}), 201

# ----------- LOGIN -----------
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "credenciales inválidas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token, "user": user.serialize()}), 200

# ----------- PRIVATE -----------
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"msg": f"Hola {user.email}", "user": user.serialize()}), 200

# ----------- VERIFY -----------
@api.route('/verify', methods=['GET'])
@jwt_required(optional=True)
def verify():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"valid": False}), 401
    return jsonify({"valid": True, "user_id": user_id}), 200
