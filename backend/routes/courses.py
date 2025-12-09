from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, User, Course

courses_bp = Blueprint("courses", __name__)

def get_or_create_dummy_user():
    user = User.query.filter_by(email="test@example.com").first()
    if user is None:
        user = User(email="test@example.com", name="Test User")
        db.session.add(user)
        db.session.commit()
    return user

@courses_bp.route("", methods=["GET"])
def list_courses():
    user = get_or_create_dummy_user()
    courses = Course.query.filter_by(user_id=user.id).all()

    data = []
    for c in courses:
        data.append({
            "id": c.id,
            "name": c.name,
            "termStart": c.term_start.isoformat(),
            "termEnd": c.term_end.isoformat(),
            "mainExamDate": c.main_exam_date.isoformat() if c.main_exam_date else None,
        })

    return jsonify(data)

@courses_bp.route("", methods=["POST"])
def create_course():
    user = get_or_create_dummy_user()
    body = request.get_json()

    name = body.get("name")
    term_start = datetime.fromisoformat(body.get("termStart")).date()
    term_end = datetime.fromisoformat(body.get("termEnd")).date()
    main_exam_date_str = body.get("mainExamDate")

    main_exam_date = None
    if main_exam_date_str:
        main_exam_date = datetime.fromisoformat(main_exam_date_str).date()

    course = Course(
        user_id=user.id,
        name=name,
        term_start=term_start,
        term_end=term_end,
        main_exam_date=main_exam_date,
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({"id": course.id}), 201