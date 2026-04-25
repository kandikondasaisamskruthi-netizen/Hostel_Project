from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
        username = request.form.get('username')
        password = request.form.get('password')

        # Student login condition:
        # Username and Password should be same
        if username == password and username != "":
            return redirect(url_for('student_dashboard'))
        else:
            return "Invalid Student Login"

    return render_template("Student_login.html")


@app.route('/student_dashboard')
def student_dashboard():
    return render_template("Student_dashboard.html")


@app.route('/complaint')
def complaint():
    return render_template("Complaint.html")


@app.route('/menu')
def menu():
    return render_template("Menu.html")


@app.route('/rating')
def rating():
    return render_template("Rating.html")


@app.route('/status')
def status():
    return render_template("Status.html")


# =========================
# ADMIN LOGIN
# =========================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Admin login condition:
        # username = admin
        # password = admin
        if username == "admin" and password == "admin":
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Admin Login"

    return render_template("Admin_login.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("Admin_Dashboard.html")


@app.route('/view_complaints')
def view_complaints():
    return render_template("View_Complaints.html")


@app.route('/update_menu')
def update_menu():
    return render_template("Update_Menu.html")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
