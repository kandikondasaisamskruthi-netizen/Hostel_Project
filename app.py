from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hostel_food_secret"


# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return render_template("home.html")


# =========================
# STUDENT LOGIN
# =========================

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        password = request.form.get('password')

        # Roll Number and Password should be same
        if roll_no == password and roll_no != "":
            session['student'] = roll_no
            return redirect(url_for('student_dashboard'))
        else:
            return "Invalid Student Login"

    return render_template("Student_login.html")


@app.route('/student_dashboard')
def student_dashboard():
    if 'student' not in session:
        return redirect(url_for('student_login'))

    return render_template("Student_dashboard.html")


# =========================
# STUDENT MODULES
# =========================

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if 'student' not in session:
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        return redirect(url_for('status'))

    return render_template("Complaint.html")


@app.route('/menu')
def menu():
    if 'student' not in session:
        return redirect(url_for('student_login'))

    menu_data = [
        ("Monday", "Idli", "Rice + Curry", "Chapati"),
        ("Tuesday", "Dosa", "Biryani", "Fried Rice"),
        ("Wednesday", "Upma", "Dal Rice", "Noodles"),
        ("Thursday", "Poori", "Meals", "Chapati"),
        ("Friday", "Pongal", "Pulihora", "Rice"),
        ("Saturday", "Vada", "Veg Rice", "Paratha"),
        ("Sunday", "Masala Dosa", "Special Meals", "Biryani")
    ]

    return render_template("Menu.html", menu_data=menu_data)


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    if 'student' not in session:
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        return redirect(url_for('student_dashboard'))

    return render_template("Rating.html")


@app.route('/status')
def status():
    if 'student' not in session:
        return redirect(url_for('student_login'))

    data = [
        ("Food Quality Issue", "Pending"),
        ("Room is not clean", "Resolved")
    ]

    return render_template("status.html", data=data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# =========================
# ADMIN LOGIN
# =========================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "admin":
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Admin Login"

    return render_template("Admin_login.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("Admin_Dashboard.html")


# =========================
# ADMIN MODULES
# =========================

@app.route('/view_complaints')
def view_complaints():
    complaints = [
        (1, "22B81A0501", "Food Quality Issue", "Pending"),
        (2, "22B81A0502", "Room is not clean", "Resolved")
    ]

    return render_template("view_complaints.html", complaints=complaints)


@app.route('/resolve/<int:id>')
def resolve(id):
    return redirect(url_for('view_complaints'))


@app.route('/update_menu', methods=['GET', 'POST'])
def update_menu():
    ratings = [
        (1, "22B81A0501", "Excellent"),
        (2, "22B81A0502", "Good"),
        (3, "22B81A0503", "Average")
    ]

    if request.method == 'POST':
        return redirect(url_for('update_menu'))

    return render_template("update_menu.html", ratings=ratings)


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
