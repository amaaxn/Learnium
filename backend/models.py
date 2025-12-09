from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)

    courses = db.relationship("Course", backref="user", lazy=True)

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    term_start = db.Column(db.Date, nullable=False)
    term_end = db.Column(db.Date, nullable=False)
    main_exam_date = db.Column(db.Date, nullable=True)

    materials = db.relationship("Material", backref="course", lazy=True)
    study_tasks = db.relationship("StudyTask", backref="course", lazy=True)

class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=True)
    raw_text = db.Column(db.Text, nullable=True)

    # Optional: store simple topic segmentation later
    metadata_json = db.Column(db.Text, nullable=True)

class StudyTask(db.Model):
    __tablename__ = "study_tasks"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    # link back to material if relevant
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"), nullable=True)
    material = db.relationship("Material", backref="tasks", lazy=True)