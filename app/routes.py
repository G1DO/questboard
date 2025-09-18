from flask import Blueprint, jsonify

bp = Blueprint("core", __name__)


@bp.get("/health")
def health():
    return jsonify(status="ok"), 200


@bp.get("/")
def index():
    return jsonify(app="QuestBoard", message="Welcome!"), 200