from datetime import datetime
from flask import Blueprint, jsonify, request
from .extensions import db
from .models import User, Quest, Submission, Score, week_start_for

api_bp = Blueprint("api", __name__)

@api_bp.post("/users")
def create_user():
    data = request.get_json() or {}
    email = data.get("email")
    display_name = data.get("display_name")
    if not email or not display_name:
        return jsonify(error="email and display_name are required"), 400
    u = User(email=email, display_name=display_name)
    db.session.add(u)
    db.session.commit()
    return jsonify(id=u.id, email=u.email, display_name=u.display_name), 201

@api_bp.get("/quests")
def list_quests():
    rows = Quest.query.order_by(Quest.starts_on.desc()).all()
    return jsonify([
        {
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "starts_on": q.starts_on.isoformat(),
            "ends_on": q.ends_on.isoformat(),
            "points": q.points,
        } for q in rows
    ])

@api_bp.post("/quests")
def create_quest():
    data = request.get_json() or {}
    try:
        q = Quest(
            title=data["title"],
            description=data.get("description", ""),
            starts_on=datetime.fromisoformat(data["starts_on"]).date(),
            ends_on=datetime.fromisoformat(data["ends_on"]).date(),
            points=int(data.get("points", 10)),
        )
    except Exception as e:
        return jsonify(error=str(e)), 400
    db.session.add(q)
    db.session.commit()
    return jsonify(id=q.id), 201

@api_bp.post("/submissions")
def create_submission():
    data = request.get_json() or {}
    s = Submission(
        user_id=data.get("user_id"),
        quest_id=data.get("quest_id"),
        text=data.get("text", ""),
        image_url=data.get("image_url"),
        status="pending",
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(id=s.id, status=s.status), 201

@api_bp.post("/submissions/<int:submission_id>/approve")
def approve_submission(submission_id: int):
    s = Submission.query.get_or_404(submission_id)
    s.status = "approved"
    db.session.add(s)

    week = week_start_for(datetime.utcnow())
    score = Score.query.filter_by(user_id=s.user_id, week_start=week).first()
    if not score:
        score = Score(user_id=s.user_id, week_start=week, points=0)
        db.session.add(score)
    score.points += s.quest.points

    db.session.commit()
    return jsonify(id=s.id, status=s.status)

@api_bp.get("/leaderboard")
def leaderboard():
    week = week_start_for(datetime.utcnow())
    rows = (
        db.session.query(Score, User)
        .join(User, User.id == Score.user_id)
        .filter(Score.week_start == week)
        .order_by(Score.points.desc())
        .limit(20)
        .all()
    )
    return jsonify([{"user": u.display_name, "points": s.points} for s, u in rows])
