from flask import Flask,redirect,flash,render_template,session,url_for,abort, request,jsonify
from database.database import create_db,get_db_connection
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
from routes.decorators import login_required

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
@login_required
def dashboard():

    user = session["user"]
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select name from users where email=?",(user,))

    result=cursor.fetchone()
    conn.close()

    if not result:
        session.pop("user", None)
        flash("User account no longer exists")
        return redirect(url_for("home"))

    return render_template("dashboard.html", user=user,name=result[0])

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500

@app.route("/api/test", methods=["POST"])
def api_test():
    data = request.json

    name = data.get("name")
    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    return jsonify({
        "name": name,
        "email": email
    }), 200

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Flask API is running"
    })
create_db()


if __name__=="__main__":
    app.run(debug=True)