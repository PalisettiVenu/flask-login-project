from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database.database import get_db_connection
from routes.decorators import login_required

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
            flash("Name is contain only letters and spaces")
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


