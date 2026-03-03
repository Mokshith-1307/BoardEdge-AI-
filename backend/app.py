from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import json

app = Flask(__name__)
app.secret_key = "boardedge_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "boardedge.db")


# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        subject TEXT,
        marks INTEGER,
        risk TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- LOGIC ---------------- #

def calculate_risk(marks):
    if marks >= 85:
        return "Low"
    elif marks >= 60:
        return "Medium"
    else:
        return "High"
def get_user_marks(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT marks FROM history WHERE username=?", (username,))
    data = cursor.fetchall()
    conn.close()
    return [m[0] for m in data]

def selection_probability(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT marks FROM history WHERE username=?", (username,))
    data = cursor.fetchall()
    conn.close()

    if not data:
        return 50

    marks = [m[0] for m in data]
    avg = sum(marks) / len(marks)

    if avg >= 85:
        return 90
    elif avg >= 70:
        return 75
    else:
        return 60


# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    marks = get_user_marks(session["username"])
    probability = selection_probability(session["username"])

    return render_template("index.html",
                           user=session["username"],
                           marks=marks,
                           probability=probability)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
                           (username, password))
            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "username" not in session:
        return redirect("/login")

    subject = request.form["subject"]
    marks = int(request.form["marks"])

    # Calculate risk
    risk = calculate_risk(marks)

    # Save to database (INCLUDING USERNAME)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history(username, subject, marks, risk) VALUES (?, ?, ?, ?)",
        (session["username"], subject, marks, risk)
    )
    conn.commit()
    conn.close()

    # Calculate selection probability
    probability = selection_probability(session["username"])

    # Motivation Message
    if marks >= 90:
        motivation = "🌟 Outstanding performance! Now aim for full 100 next time!"
    elif marks >= 75:
        motivation = "🚀 Great job! Push a little more and aim for excellence!"
    elif marks >= 50:
        motivation = "💪 Good effort! Revise weak areas and improve further!"
    else:
        motivation = "📚 Don't worry! Focus on fundamentals and aim to pass strongly!"

    return render_template(
        "result.html",
        subject=subject,
        marks=marks,
        risk=risk,
        probability=probability,
        motivation=motivation
    )
@app.route("/history")
def history():
    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT subject, marks, risk FROM history WHERE username=?",
        (session["username"],)
    )
    data = cursor.fetchall()
    conn.close()

    return render_template("history.html", data=data)
@app.route("/leaderboard")
def leaderboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, MAX(marks) FROM history GROUP BY username ORDER BY MAX(marks) DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return render_template("leaderboard.html", data=data)


@app.route("/profile")
def profile():
    return render_template("profile.html", user=session["username"])


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/mentor")
def mentor():
    return render_template("mentor.html")


@app.route("/papers")
def papers():
    return render_template("papers.html")


@app.route("/formulas")
def formulas():
    return render_template("formulas.html")


@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM history")
    total_tests = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM history")
    avg = cursor.fetchone()[0] or 0

    cursor.execute("SELECT risk, COUNT(*) FROM history GROUP BY risk")
    risk_data = cursor.fetchall()

    conn.close()

    return render_template("admin.html",
                           total_users=total_users,
                           total_tests=total_tests,
                           avg=round(avg, 2),
                           risk_data=json.dumps(risk_data))


if __name__ == "__main__":
    app.run()