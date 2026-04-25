from flask import Flask, render_template, request, redirect, session
import sqlite3
import sqlite3

app = Flask(__name__)
app.secret_key = "hostel_secret_key"

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Complaints table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        complaint TEXT,
        status TEXT
    )
    """)

    # Ratings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        rating TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- STUDENT LOGIN ----------------
@app.route("/student_login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Username and password should be same
        if username == password:
            session["student"] = username
            return redirect("/student_dashboard")
        else:
            return "Invalid Login"

    return render_template("student_login.html")


# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student_dashboard")
def student_dashboard():
    if "student" not in session:
        return redirect("/student_login")

    return render_template(
        "student_dashboard.html",
        roll_no=session.get("student")
    )


# ---------------- COMPLAINT ----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if request.method == "POST":
        complaint_text = request.form["complaint"]
        roll_no = session.get("student")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
    INSERT INTO complaints (roll_no, complaint, status)
    VALUES (?, ?, ?)
    """, (roll_no, complaint_text, "Pending"))

        conn.commit()
        conn.close()

        return redirect("/status")

    return render_template("Complaint.html")

# ---------------- MENU ----------------
@app.route("/menu")
def menu():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT day, breakfast, lunch, dinner
        FROM menu
        ORDER BY CASE day
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6
            WHEN 'Sunday' THEN 7
        END
    """)

    menu_data = cur.fetchall()

    conn.close()

    return render_template("Menu.html", menu_data=menu_data)

# ---------------- RATING ----------------
@app.route("/rating", methods=["GET", "POST"])
def rating():
    if request.method == "POST":
        rating_value = request.form["rating"]
        roll_no = session.get("student")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT,
                rating TEXT
            )
        """)

        cur.execute("""
            INSERT INTO ratings (roll_no, rating)
            VALUES (?, ?)
        """, (roll_no, rating_value))

        conn.commit()
        conn.close()

        return redirect("/student_dashboard")

    return render_template("rating.html")


# ---------------- STATUS ----------------
@app.route("/status")
def status():
    if "student" not in session:
        return redirect("/student_login")

    roll_no = session["student"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT complaint, status
        FROM complaints
        WHERE roll_no = ?
        ORDER BY id DESC
    """, (roll_no,))

    data = cur.fetchall()

    conn.close()

    return render_template("status.html", data=data)


# ---------------- ADMIN LOGIN ----------------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin@123" and password == "admin@123":
            session["admin"] = username
            return redirect("/admin_dashboard")
        else:
            return '''
            <script>
                alert("Invalid Admin Credentials");
                window.location.href="/admin_login";
            </script>
            '''

    return render_template("admin_login.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin_login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT id, roll_no, complaint, status FROM complaints")
    complaints = cur.fetchall()

    conn.close()

    return render_template("admin_dashboard.html", complaints=complaints)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    breakfast TEXT,
    lunch TEXT,
    dinner TEXT
)
""")

cur.execute("DELETE FROM menu")

weekly_menu = [
    ("Monday", "Idli, Sambar", "Rice, Dal, Potato Curry", "Chapati, Rice, Paneer Curry"),
    ("Tuesday", "Dosa, Chutney", "Veg Biryani", "Rice, Sambar"),
    ("Wednesday", "Poori, Curry", "Fried Rice", "Chapati, Rice, Chicken, Paneer"),
    ("Thursday", "Upma, Chutney", "Rice, Rasam", "Rice, Vegetable Curry"),
    ("Friday", "Pongal, Sambar", "Jeera Rice, Dal", "Chapati, Rice, Veg Curry"),
    ("Saturday", "Vada, Idli", "Pulihora, Rice, Curry", "Rice, Curry"),
    ("Sunday", "Khichdi", "Chicken Biryani, Veg Biryani", "Rice, Brinjal Curry, Sweet")
]

cur.executemany("""
INSERT INTO menu (day, breakfast, lunch, dinner)
VALUES (?, ?, ?, ?)
""", weekly_menu)


@app.route("/view_complaints")
def view_complaints():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM complaints
        WHERE status = 'Pending'
    """)

    complaints = cur.fetchall()

    conn.close()

    return render_template("view_complaints.html", complaints=complaints)
@app.route("/resolve/<int:id>")
def resolve(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE complaints
        SET status = 'Resolved'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/view_complaints")

@app.route("/update_menu", methods=["GET", "POST"])
def update_menu():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        day = request.form["day"]
        breakfast = request.form["breakfast"]
        lunch = request.form["lunch"]
        dinner = request.form["dinner"]

        cur.execute("""
            SELECT breakfast, lunch, dinner
            FROM menu
            WHERE day = ?
        """, (day,))

        old_data = cur.fetchone()

        if old_data:
            if breakfast == "":
                breakfast = old_data[0]
            if lunch == "":
                lunch = old_data[1]
            if dinner == "":
                dinner = old_data[2]

            cur.execute("""
                UPDATE menu
                SET breakfast = ?, lunch = ?, dinner = ?
                WHERE day = ?
            """, (breakfast, lunch, dinner, day))

            conn.commit()

    cur.execute("SELECT id, roll_no, rating FROM ratings ORDER BY id DESC")
    ratings = cur.fetchall()

    conn.close()

    return render_template("update_menu.html", ratings=ratings)
conn.commit()
conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
