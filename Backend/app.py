from flask import Flask, jsonify
from functools import wraps
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from db import db
from model import User

from auth import auth_bp
from a2_company_routes import company_bp
from a3_student_routes import student_bp
from a1_admin_routes import admin_bp






def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-jwt-key"

    db.init_app(app)
    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth_bp) # Register auth blueprint
    app.register_blueprint(company_bp) 
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp) 


    with app.app_context():
        db.create_all()







        # Auto create admin ===================
        if not User.query.filter_by(email="admin@gmail.com").first():
            admin = User(
                name="Admin User",
                email="admin@gmail.com",
                password="pbkdf2:sha256:600000$auto$hashed",  # placeholder
                role="admin"
            )
            from werkzeug.security import generate_password_hash
            admin.password = generate_password_hash("admin123")

            db.session.add(admin)
            db.session.commit()
            print(" Admin created!")

            

        # RWA in ROUTE =================
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

if __name__ == "__main__":
    app.run(debug=True)