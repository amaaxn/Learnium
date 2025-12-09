from flask import Blueprint

plans_bp = Blueprint("plans", __name__)

@plans_bp.route("/generate/<int:course_id>", methods=["POST"])
def generate_plan(course_id):
    # later: call planner service and create StudyTask rows
    return {"message": f"will generate plan for course {course_id}"}