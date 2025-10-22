from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import User
from .schemas import RegisterIn, LoginIn


auth_bp = Blueprint("auth", __name__)




@auth_bp.post("/register")
def register():
    try:
        data = RegisterIn(**(request.get_json() or {}))
    except Exception as e:
        return jsonify(error="invalid input", detail=str(e)), 400


    u = User(email=str(data.email), display_name=data.display_name)
    u.set_password(data.password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="email already registered"), 409


    return jsonify(id=u.id, email=u.email, display_name=u.display_name), 201




@auth_bp.post("/login")
def login():
    try:
        data = LoginIn(**(request.get_json() or {}))
    except Exception as e:
        return jsonify(error="invalid input", detail=str(e)), 400


    u = User.query.filter_by(email=str(data.email)).first()
    if not u or not u.check_password(data.password):
        return jsonify(error="invalid credentials"), 401


    access_token = create_access_token(identity=str(u.id))  # <- make it a string
    resp = make_response(jsonify(access_token=access_token, user={"id": u.id, "display_name": u.display_name}))
    set_access_cookies(resp, access_token)
    return resp




@auth_bp.post("/logout")
@jwt_required()
def logout():
    resp = make_response(jsonify(msg="logged out"))
    unset_jwt_cookies(resp)
    return resp




@auth_bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    u = User.query.get_or_404(int(uid))  # <- cast back to int
    return jsonify(id=u.id, email=u.email, display_name=u.display_name)