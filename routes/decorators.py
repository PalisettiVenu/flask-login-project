from functools import wraps
from flask import session, flash, redirect, url_for
from database.database import get_db_connection

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
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

        result = cursor.fetchone()
        conn.close()

        if not result or result[0] != "admin":
            flash("Access denied")
            return redirect(url_for("dashboard"))

        return func(*args, **kwargs)

    return wrapper