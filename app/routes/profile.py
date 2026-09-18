from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models.profile import Profile, HouseholdMember, Allergy, DietaryPreference

profile_bp = Blueprint("profile", __name__)

# Fixed lists shown as checkboxes on the form. Keep these here (not in the
# database) since they're just the *options* — the choices the user makes
# are what get saved as rows.
COMMON_ALLERGIES = ["Peanuts", "Tree nuts", "Dairy", "Gluten", "Shellfish", "Eggs"]
DIET_OPTIONS = ["Halal", "Vegetarian", "Vegan", "Kosher"]


@profile_bp.route("/profile/setup", methods=["GET", "POST"])
@login_required
def setup():
    existing = current_user.profile  # None the first time, a Profile after that

    if request.method == "POST":
        age = request.form.get("age", type=int)
        is_student = "is_student" in request.form

        # Students are treated as living alone (see the reasoning behind
        # this decision) — so the "who do you live with" section is
        # skipped entirely for them, regardless of what was in the form.
        if is_student:
            lives_alone = True
        else:
            lives_alone = request.form.get("lives_alone") == "yes"

        monthly_budget = request.form.get("monthly_budget", type=float)

        if not age:
            flash("Please enter a valid age.", "danger")
            return redirect(url_for("profile.setup"))

        # Update in place if a profile already exists, otherwise create one.
        if existing:
            profile = existing
            profile.age = age
            profile.is_student = is_student
            profile.lives_alone = lives_alone
            profile.monthly_budget = monthly_budget
            # Clear out the old related rows — simplest way to handle an
            # edit is to replace them rather than try to match old to new.
            profile.household_members.clear()
            profile.allergies.clear()
            profile.dietary_preferences.clear()
        else:
            profile = Profile(
                user_id=current_user.id,
                age=age,
                is_student=is_student,
                lives_alone=lives_alone,
                monthly_budget=monthly_budget,
            )
            db.session.add(profile)

        # Household members — only collected when not living alone.
        if not lives_alone:
            member_ages = request.form.getlist("member_age[]")
            member_genders = request.form.getlist("member_gender[]")
            for age_val, gender_val in zip(member_ages, member_genders):
                if age_val.strip():
                    profile.household_members.append(
                        HouseholdMember(age=int(age_val), gender=gender_val)
                    )

        # Allergies — checked common ones, plus any typed into "other".
        for allergy_name in request.form.getlist("allergy[]"):
            profile.allergies.append(Allergy(name=allergy_name))

        other_allergies = request.form.get("allergy_other", "")
        for name in other_allergies.split(","):
            name = name.strip()
            if name:
                profile.allergies.append(Allergy(name=name))

        # Dietary preferences — ticked boxes, one row each.
        for diet_name in request.form.getlist("diet[]"):
            profile.dietary_preferences.append(DietaryPreference(name=diet_name))

        db.session.commit()
        flash("Profile saved.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template(
        "profile_setup.html",
        profile=existing,
        common_allergies=COMMON_ALLERGIES,
        diet_options=DIET_OPTIONS,
    )
