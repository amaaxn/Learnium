from flask import Flask
from flask_cors import CORS
from models import db, init_db
from routes.courses import courses_bp
from routes.materials import materials_bp
from routes.plans import plans_bp

def create_app():
    app = Flask(__name__)
    CORS(app, origins="http://localhost:5173", supports_credentials=True)

    # For dev: SQLite. Once you want Postgres, change the URI.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///study_coach.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)

    app.register_blueprint(courses_bp, url_prefix="/api/courses")
    app.register_blueprint(materials_bp, url_prefix="/api/materials")
    app.register_blueprint(plans_bp, url_prefix="/api/plans")

    @app.route("/api/health")
    def health():
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)