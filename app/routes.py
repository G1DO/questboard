from flask import Blueprint, jsonify
bp = Blueprint("core", __name__)

@bp.get("/health")
def health():
    return jsonify(status="ok"), 200

# CHANGED: was "/", move it to "/api" (or "/api/info")
@bp.get("/api")
def api_root():
    return jsonify(app="QuestBoard", message="Welcome!"), 200
