from flask import Flask,redirect,flash,render_template,session,url_for
from database.database import create_db,get_db_connection
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp

import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        flash("Please login first")
        return redirect(url_for("home"))

    user = session["user"]
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select name from users where email=?",(user,))

    result=cursor.fetchone()
    conn.close()

    return render_template("dashboard.html", user=user,name=result[0])


create_db()


if __name__=="__main__":
    app.run(debug=True)