"""
BudgetBite app factory.
Everything (frontend templates + backend routes) is served from this
one Flask app, so you can test both sides together with one `python run.py`.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Extensions are created here (uninitialized) so models.py can import `db`
# without causing circular imports.
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # Where Flask-Login sends users who try to access a @login_required
    # page without being logged in.
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from app.models.user import User
    # Importing these here (even though nothing below calls them directly)
    # is what makes db.create_all() below know these tables exist.
    from app.models.profile import Profile, HouseholdMember, Allergy, DietaryPreference

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints (route groups)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)

    with app.app_context():
        db.create_all()  # creates budgetbite.db + tables on first run

    return app
