from flask import Flask, jsonify
from functools import wraps
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from extensions import mail
from db import db
from model import User
from celery_config import make_celery

from auth import auth_bp
from a2_company_routes import company_bp
from a3_student_routes import student_bp
from a1_admin_routes import admin_bp



def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-jwt-key"

    # Mail config
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "ypasnshiv@gmail.com"      # ← your Gmail
    app.config["MAIL_PASSWORD"] = "hqmmubxifscbdylc"        # ← Gmail App Password
    app.config["MAIL_DEFAULT_SENDER"] = "ypasnshiv@gmail.com"

    db.init_app(app)
    mail.init_app(app)
    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@gmail.com").first():
            from werkzeug.security import generate_password_hash
            admin = User(
                name="Admin User",
                email="admin@gmail.com",
                password=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created!")

        def role_required(role):
            def decorator(fn):
                @wraps(fn)
                def wrapper(*args, **kwargs):
                    user_id = get_jwt_identity()
                    user = User.query.get(user_id)
                    if not user or user.role != role:
                        return jsonify({"error": f"{role} only"}), 403
                    return fn(*args, **kwargs)
                return wrapper
            return decorator

    return app


app = create_app()
celery = make_celery(app)   # ← Celery instance

app.config.update(
    CELERY_BROKER_URL="redis://localhost:6379/0",
    CELERY_RESULT_BACKEND="redis://localhost:6379/0"
)

if __name__ == "__main__":
    app.run(debug=True)