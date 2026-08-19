from flask import Blueprint, redirect, url_for, flash, session, render_template
from database.database import get_db_connection
from routes.decorators import admin_required, login_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, role FROM users"
    )

    users = cursor.fetchall()
    conn.close()

    return render_template("admin.html", users=users)

@admin_bp.route("/admin/users/<int:user_id>/make-admin", methods=["POST"])
@login_required
@admin_required
def make_admin(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET role = ? WHERE ID = ?",
        ("admin", user_id)
    )
    conn.commit()
    conn.close()

    flash("User promoted to admin sucessfully")
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/users/<int:user_id>/make-user", methods=["POST"])
@login_required
@admin_required
def make_user(user_id):

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (user,)
    )

    current_user = cursor.fetchone()

    if current_user[0] == user_id:
        conn.close()
        flash("You cannot demote yourself")
        return redirect(url_for("admin.admin_dashboard"))

    cursor.execute(
        "UPDATE users SET role = ? WHERE id = ?",
        ("user", user_id)
    )

    conn.commit()
    conn.close()

    flash("User demoted to user successfully")
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (user,)
    )

    current_user = cursor.fetchone()

    if current_user[0] == user_id:
        conn.close()
        flash("You cannot delete yourself")
        return redirect(url_for("admin.admin_dashboard"))

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    flash("User deleted successfully")
    return redirect(url_for("admin.admin_dashboard"))





