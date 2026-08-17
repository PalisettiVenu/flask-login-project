from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    email=request.form['email']
    password=request.form['password']

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
    print(user)
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
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name:
            flash("Name is required")
            return render_template("register.html")
        if not email:
            flash("Email is required")
            return render_template("register.html")
        if not password:
            flash("password is required")
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
            "INSERT INTO users(name,email, password) VALUES(?, ?, ?)",
            (name,email, hashed_password)
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