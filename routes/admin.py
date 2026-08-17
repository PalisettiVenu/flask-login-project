from flask import Blueprint, redirect, url_for, flash, session, render_template
from database.database import get_db_connection
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_dashboard():
    if "user" not in session:
        flash("Please login first")
        return redirect(url_for("home"))

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE email = ?",
        (user,)
    )

    result=cursor.fetchone()

    if not result or result[0] != "admin":
        flash("Access denied")
        return redirect(url_for("dashboard"))

    cursor.execute(
        "SELECT id, name, email, role FROM users"
    )

    users = cursor.fetchall()
    conn.close()

    return render_template("admin.html", users=users)

@admin_bp.route("/admin/users/<int:user_id>/make-admin", methods=["POST"])
def make_admin(user_id):
    if "user" not in session:
        flash("Please login first")
        return redirect(url_for("home"))




