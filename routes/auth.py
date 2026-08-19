from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import get_db_connection
import re

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    email=request.form.get('email', '').strip().lower()
    password=request.form.get('password','')

    if not email:
        flash("Email is required")
        return redirect(url_for("home"))
    if not password:
        flash("password is required")
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password,role FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        if check_password_hash(user[0],password):
            session["user"] = email
            flash("Login successful")
            return redirect(url_for("dashboard"))

    flash("Invalid email or password")
    return redirect(url_for("home"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name=request.form['name']
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name:
            flash("Name is required")
            return render_template("register.html")
        if not re.match(r"^[A-Za-z ]+$", name):
            flash("Name can contain only letters and spaces")
            return render_template("register.html")

        if not email:
            flash("Email is required")
            return render_template("register.html")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Please enter a valid email")
            return render_template("register.html")

        if not password:
            flash("password is required")
            return render_template("register.html")
        if len(password) < 8:
            flash("Password must be at least 8 characters")
            return render_template("register.html")

        if not re.search(r"[A-Z]", password):
            flash("Password must contain at least one uppercase letter")
            return render_template("register.html")

        if not re.search(r"[a-z]", password):
            flash("Password must contain at least one lowercase letter")
            return render_template("register.html")

        if not re.search(r"[0-9]", password):
            flash("Password must contain at least one number")
            return render_template("register.html")

        if not re.search(r"[^A-Za-z0-9]", password):
            flash("Password must contain at least one special character")
            return render_template("register.html")

        if not confirm_password:
            flash("confirm password is required")
            return render_template("register.html")
        if password!=confirm_password:
            flash("confirm password didn't match")
            return render_template("register.html")

        conn = get_db_connection()
        cursor=conn.cursor()

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        user=cursor.fetchone()

        if user:
            flash("Email already exists")
            conn.close()
            return redirect(url_for("auth.register"))

        cursor.execute(
            "INSERT INTO users(name,email, password, role) VALUES(?, ?, ?, ?)",
            (name,email, hashed_password, "user")
        )

        conn.commit()
        conn.close()
        flash("Registration successful. Please login.")
        return redirect(url_for("home"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():

    session.pop("user", None)

    flash("Logged out successfully")

    return redirect(url_for("home"))