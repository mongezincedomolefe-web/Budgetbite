from app import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    is_student = db.Column(db.Boolean, default=False)
    lives_alone = db.Column(db.Boolean, default=True)  # ignored/true when is_student is True
    monthly_budget = db.Column(db.Float)

    # backref lets you do current_user.profile from anywhere
    user = db.relationship("User", backref=db.backref("profile", uselist=False))

    # cascade="all, delete-orphan" means: delete the profile, and every
    # household member / allergy / diet row tied to it goes too.
    household_members = db.relationship(
        "HouseholdMember", backref="profile", cascade="all, delete-orphan"
    )
    allergies = db.relationship(
        "Allergy", backref="profile", cascade="all, delete-orphan"
    )
    dietary_preferences = db.relationship(
        "DietaryPreference", backref="profile", cascade="all, delete-orphan"
    )


class HouseholdMember(db.Model):
    __tablename__ = "household_members"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)


class Allergy(db.Model):
    __tablename__ = "allergies"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)


class DietaryPreference(db.Model):
    __tablename__ = "dietary_preferences"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
