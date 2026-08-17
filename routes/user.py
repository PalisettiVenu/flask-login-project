from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database.database import get_db_connection

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile")
def profile():
    if "user" not in session:
        flash("Please login first")
        return redirect(url_for("home"))
    user = session["user"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("select name,email from users where email=?", (user,))
    result = cursor.fetchone()
    conn.close()

    return render_template("profile.html", name=result[0],email=result[1])

@user_bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user" not in session:
        flash("Please login first")
        return redirect(url_for("home"))
    user = session["user"]
    if request.method == "POST":
        new_name = request.form['name']
        if not new_name:
            flash("Name is required")
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


