from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database.database import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash
from routes.decorators import login_required
import re

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile")
@login_required
def profile():

    user = session["user"]
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select name,email from users where email=?", (user,))

    result = cursor.fetchone()
    conn.close()

    return render_template("profile.html", name=result[0],email=result[1])

@user_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    user = session["user"]

    if request.method == "POST":
        new_name = request.form.get('name',"").strip()
        if not new_name:
            flash("Name is required")
            return render_template("edit_profile.html")

        if not new_name.replace(" ", "").isalpha():
            flash("Name can contain only letters and spaces")
            return render_template("edit_profile.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET name = ? WHERE email = ?",
            (new_name, user)
        )

        conn.commit()
        conn.close()

        flash("Profile updated successfully")
        return redirect(url_for("user.profile"))

    return render_template("edit_profile.html")

@user_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        user = session["user"]
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")
        if not current_password:
            flash("Current password is required")
            return render_template("change_password.html")

        if not new_password:
            flash("New password is required")
            return render_template("change_password.html")

        if not confirm_password:
            flash("Confirm password is required")
            return render_template("change_password.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE email = ?",
            (user,)
        )

        result = cursor.fetchone()

        if not result:
            conn.close()
            session.pop("user", None)
            flash("User account no longer exists")
            return redirect(url_for("home"))

        if not check_password_hash(result[0], current_password):
            conn.close()
            flash("Current password is incorrect")
            return render_template("change_password.html")

        if new_password == current_password:
            conn.close()
            flash("New password must be different from current password")
            return render_template("change_password.html")

        if new_password != confirm_password:
            conn.close()
            flash("New passwords do not match")
            return render_template("change_password.html")

        if len(new_password) < 8:
            conn.close()
            flash("Password must be at least 8 characters")
            return render_template("change_password.html")

        if not re.search(r"[A-Z]", new_password):
            conn.close()
            flash("Password must contain at least one uppercase letter")
            return render_template("change_password.html")

        if not re.search(r"[a-z]", new_password):
            conn.close()
            flash("Password must contain at least one lowercase letter")
            return render_template("change_password.html")

        if not re.search(r"[0-9]", new_password):
            conn.close()
            flash("Password must contain at least one number")
            return render_template("change_password.html")

        if not re.search(r"[^A-Za-z0-9]", new_password):
            conn.close()
            flash("Password must contain at least one special character")
            return render_template("change_password.html")

        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (hashed_password, user)
        )

        conn.commit()
        conn.close()

        flash("Password changed successfully")
        return redirect(url_for("user.profile"))

    return render_template("change_password.html")

@user_bp.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        user = session["user"]
        password = request.form.get("password", "")
        confirm_delete = request.form.get("confirm_delete")

        if not password:
            flash("Password is required")
            return render_template("delete_account.html")

        if not confirm_delete:
            flash("Please confirm that you want to delete your account")
            return render_template("delete_account.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE email = ?",
            (user,)
        )

        result = cursor.fetchone()

        if not result:
            conn.close()
            session.pop("user", None)
            flash("User account no longer exists")
            return redirect(url_for("home"))

        if not check_password_hash(result[0], password):
            conn.close()
            flash("Incorrect password")
            return render_template("delete_account.html")

        cursor.execute(
            "DELETE FROM users WHERE email = ?",
            (user,)
        )
        conn.commit()
        conn.close()

        session.pop("user", None)
        flash("Account deleted successfully")
        return redirect(url_for("home"))

    return render_template("delete_account.html")

