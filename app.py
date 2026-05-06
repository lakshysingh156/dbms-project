import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "resume_shortlisting.db"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "resume-shortlisting-demo-secret")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            skills TEXT NOT NULL,
            experience_years REAL NOT NULL DEFAULT 0,
            education TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            min_experience REAL NOT NULL DEFAULT 0,
            description TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            resume_url TEXT,
            match_score REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Under Review',
            reviewer_notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(candidate_id) REFERENCES candidates(id),
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        );
        """
    )
    db.commit()
    db.close()


init_db()


def seed_demo_data():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    now = datetime.utcnow().isoformat()

    candidate_count = db.execute("SELECT COUNT(*) AS total FROM candidates").fetchone()["total"]
    job_count = db.execute("SELECT COUNT(*) AS total FROM jobs").fetchone()["total"]
    app_count = db.execute("SELECT COUNT(*) AS total FROM applications").fetchone()["total"]

    if candidate_count == 0:
        db.executemany(
            """
            INSERT INTO candidates (full_name, email, phone, skills, experience_years, education, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Aarav Sharma",
                    "aarav.sharma@email.com",
                    "9876543210",
                    "python, sql, flask, api",
                    2.5,
                    "B.Tech CSE",
                    now,
                ),
                (
                    "Priya Mehta",
                    "priya.mehta@email.com",
                    "9811122233",
                    "java, spring, mysql, rest",
                    3.0,
                    "B.Tech IT",
                    now,
                ),
                (
                    "Rohan Singh",
                    "rohan.singh@email.com",
                    "9898989898",
                    "react, nodejs, mongodb, javascript",
                    1.8,
                    "BCA",
                    now,
                ),
                (
                    "Neha Kapoor",
                    "neha.kapoor@email.com",
                    "9765432101",
                    "python, pandas, sql, tableau",
                    2.2,
                    "MCA",
                    now,
                ),
                (
                    "Kunal Verma",
                    "kunal.verma@email.com",
                    "9788887711",
                    "django, postgresql, docker, linux",
                    3.4,
                    "B.Tech CSE",
                    now,
                ),
            ],
        )

    if job_count == 0:
        db.executemany(
            """
            INSERT INTO jobs (title, department, required_skills, min_experience, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Backend Developer",
                    "Engineering",
                    "python, sql, flask, api",
                    2.0,
                    "Develop backend services and optimize SQL queries.",
                    now,
                ),
                (
                    "Data Analyst",
                    "Analytics",
                    "sql, python, tableau, excel",
                    1.5,
                    "Analyze recruitment and business metrics.",
                    now,
                ),
                (
                    "Full Stack Developer",
                    "Product",
                    "react, nodejs, javascript, sql",
                    2.0,
                    "Build scalable frontend and backend modules.",
                    now,
                ),
                (
                    "Software Engineer",
                    "Platform",
                    "java, mysql, rest, git",
                    2.5,
                    "Build robust backend components and APIs.",
                    now,
                ),
                (
                    "Python Developer",
                    "Automation",
                    "python, django, postgresql, docker",
                    2.0,
                    "Create automation tools and internal systems.",
                    now,
                ),
            ],
        )

    if app_count == 0:
        candidate_rows = db.execute("SELECT id, skills, experience_years FROM candidates ORDER BY id LIMIT 5").fetchall()
        job_rows = db.execute("SELECT id, required_skills, min_experience FROM jobs ORDER BY id LIMIT 5").fetchall()
        for candidate, job in zip(candidate_rows, job_rows):
            score, status = calculate_match_score(candidate, job)
            db.execute(
                """
                INSERT INTO applications (candidate_id, job_id, resume_url, match_score, status, reviewer_notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate["id"],
                    job["id"],
                    "",
                    score,
                    status,
                    "Auto-seeded demo application.",
                    now,
                ),
            )

    db.commit()
    db.close()


def to_skill_set(skills_text):
    return {token.strip().lower() for token in skills_text.split(",") if token.strip()}


def calculate_match_score(candidate, job):
    candidate_skills = to_skill_set(candidate["skills"])
    required_skills = to_skill_set(job["required_skills"])

    skill_score = 0
    if required_skills:
        overlap = candidate_skills.intersection(required_skills)
        skill_score = (len(overlap) / len(required_skills)) * 70

    exp_score = 0
    minimum_exp = float(job["min_experience"])
    if minimum_exp <= 0:
        exp_score = 30
    else:
        exp_score = min((float(candidate["experience_years"]) / minimum_exp) * 30, 30)

    score = round(skill_score + exp_score, 2)
    status = "Shortlisted" if score >= 60 else "Rejected"
    return score, status


seed_demo_data()


@app.route("/")
def home():
    db = get_db()
    counts = {
        "candidates": db.execute("SELECT COUNT(*) AS total FROM candidates").fetchone()["total"],
        "jobs": db.execute("SELECT COUNT(*) AS total FROM jobs").fetchone()["total"],
        "applications": db.execute("SELECT COUNT(*) AS total FROM applications").fetchone()["total"],
        "shortlisted": db.execute(
            "SELECT COUNT(*) AS total FROM applications WHERE status='Shortlisted'"
        ).fetchone()["total"],
    }
    return render_template("home.html", counts=counts)


@app.route("/dashboard")
def dashboard():
    db = get_db()
    metrics = db.execute(
        """
        SELECT
            COUNT(*) AS total_apps,
            SUM(CASE WHEN status='Shortlisted' THEN 1 ELSE 0 END) AS shortlisted,
            SUM(CASE WHEN status='Rejected' THEN 1 ELSE 0 END) AS rejected,
            ROUND(AVG(match_score), 2) AS avg_score
        FROM applications
        """
    ).fetchone()

    leaderboard = db.execute(
        """
        SELECT a.id, c.full_name, j.title, a.match_score, a.status, a.created_at
        FROM applications a
        JOIN candidates c ON c.id = a.candidate_id
        JOIN jobs j ON j.id = a.job_id
        ORDER BY a.match_score DESC, a.created_at DESC
        LIMIT 8
        """
    ).fetchall()
    return render_template("dashboard.html", metrics=metrics, leaderboard=leaderboard)


@app.route("/candidates", methods=["GET", "POST"])
def candidates():
    db = get_db()
    if request.method == "POST":
        try:
            db.execute(
                """
                INSERT INTO candidates (full_name, email, phone, skills, experience_years, education, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request.form["full_name"],
                    request.form["email"],
                    request.form.get("phone", ""),
                    request.form["skills"],
                    float(request.form["experience_years"] or 0),
                    request.form.get("education", ""),
                    datetime.utcnow().isoformat(),
                ),
            )
            db.commit()
            flash("Candidate added successfully.", "success")
        except sqlite3.IntegrityError:
            flash("Candidate with this email already exists.", "error")
        return redirect(url_for("candidates"))

    rows = db.execute("SELECT * FROM candidates ORDER BY created_at DESC").fetchall()
    return render_template("candidates.html", candidates=rows)


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    db = get_db()
    if request.method == "POST":
        db.execute(
            """
            INSERT INTO jobs (title, department, required_skills, min_experience, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                request.form["title"],
                request.form["department"],
                request.form["required_skills"],
                float(request.form["min_experience"] or 0),
                request.form.get("description", ""),
                datetime.utcnow().isoformat(),
            ),
        )
        db.commit()
        flash("Job posting created.", "success")
        return redirect(url_for("jobs"))

    rows = db.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    return render_template("jobs.html", jobs=rows)


@app.route("/applications", methods=["GET", "POST"])
def applications():
    db = get_db()
    if request.method == "POST":
        candidate_id = int(request.form["candidate_id"])
        job_id = int(request.form["job_id"])

        candidate = db.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,)).fetchone()
        job = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()

        if candidate is None or job is None:
            flash("Invalid candidate or job selected.", "error")
            return redirect(url_for("applications"))

        score, status = calculate_match_score(candidate, job)
        db.execute(
            """
            INSERT INTO applications (candidate_id, job_id, resume_url, match_score, status, reviewer_notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                candidate_id,
                job_id,
                request.form.get("resume_url", ""),
                score,
                status,
                request.form.get("reviewer_notes", ""),
                datetime.utcnow().isoformat(),
            ),
        )
        db.commit()
        flash(f"Application evaluated. Score: {score}, Status: {status}.", "success")
        return redirect(url_for("applications"))

    rows = db.execute(
        """
        SELECT a.*, c.full_name, j.title AS job_title
        FROM applications a
        JOIN candidates c ON c.id = a.candidate_id
        JOIN jobs j ON j.id = a.job_id
        ORDER BY a.created_at DESC
        """
    ).fetchall()
    candidate_rows = db.execute("SELECT id, full_name FROM candidates ORDER BY full_name").fetchall()
    job_rows = db.execute("SELECT id, title FROM jobs ORDER BY title").fetchall()
    return render_template(
        "applications.html",
        applications=rows,
        candidates=candidate_rows,
        jobs=job_rows,
    )


@app.route("/reports")
def reports():
    db = get_db()
    by_department = db.execute(
        """
        SELECT j.department, COUNT(a.id) AS total,
               ROUND(AVG(a.match_score), 2) AS avg_score
        FROM jobs j
        LEFT JOIN applications a ON a.job_id = j.id
        GROUP BY j.department
        ORDER BY total DESC
        """
    ).fetchall()

    top_candidates = db.execute(
        """
        SELECT c.full_name, c.email, MAX(a.match_score) AS best_score
        FROM candidates c
        JOIN applications a ON a.candidate_id = c.id
        GROUP BY c.id
        ORDER BY best_score DESC
        LIMIT 10
        """
    ).fetchall()
    return render_template(
        "reports.html",
        by_department=by_department,
        top_candidates=top_candidates,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
