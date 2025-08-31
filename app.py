import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash
from datetime import datetime, timedelta
import db
import config
import reviews
import users
import secrets


app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    if "username" in session and "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return render_template("index.html", reviews = all_reviews)

@app.route("/find_review")
def find_review():
    title = (request.args.get("title") or "").strip()
    author = (request.args.get("author") or "").strip()

    if title or author:
        results = reviews.find_review_fields(title, author)
    else:
        results = []

    return render_template("find_review.html", title=title, author=author, results=results)

@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    if not review:
        abort(404)
    classes = reviews.get_classes(review_id)
    comments = reviews.get_comments(review_id)

    return render_template("show_review.html", review=review, classes=classes, comments=comments)

@app.route("/register")
def register():
    if "username" in session:
        return redirect("/")

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    error = False
    if len(username) < 2 or len(username) > 20:
        flash("Username must be 2-20 characters")
        error = True
    if password1 != password2:
        flash("Passwords do not match")
        error = True
    if len(password1) < 4 or len(password2) < 4:
        flash("Password must be at least 4 digits")
        error = True
    
    if error:
        return redirect("/register")

    try:
        users.create_user(username, password1)
        user_id = users.check_login(username, password1)
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
    except sqlite3.IntegrityError:
        flash("Username is already taken!")
        return redirect("/register")

    flash("Registration successful!", "success")
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    reviews = users.get_user_reviews(user_id)

    own_page = False
    if session.get("user_id") == user_id:
        own_page = True

    return render_template("show_user.html", user=user, reviews=reviews, own_page=own_page)


@app.route("/create_review", methods=["POST"])
def create_review():
    require_login()
    check_csrf()
    title = request.form["title"]
    author = request.form["author"]
    review_text = request.form["review"]
    grade = request.form["grade"]

    all_classes = reviews.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry and entry != "(select)" and ":" in entry:
            entry_title, entry_value = entry.split(":")
            if entry_title not in all_classes or entry_value not in all_classes[entry_title]:
                abort(403)
            classes.append((entry_title, entry_value))

    if not (title and author and review_text and grade):
        flash("All fields must be filled")
        return redirect("/new_review")

    try:
        grade = int(grade)
    except ValueError:
        flash("The grade must be an integer between 0 and 10.")
        return redirect("/new_review")

    if len(title) > 100:
        flash(f"Book title is {len(title)-100} characters too long.")
        return redirect("/new_review")
    if len(author) > 50:
        flash(f"Author name is {len(author)-50} characters too long.")
        return redirect("/new_review")
    if not (0 <= grade <= 10):
        flash("The grade must be between 0 and 10.")
        return redirect("/new_review")

    review_id = reviews.add_review(title, author, review_text, grade, session["user_id"], classes)
    return redirect("/review/" + str(review_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form.get("comment").strip()
    review_id = request.form.get("review_id")
    if not review_id or not comment:
        flash("Post content required")
        return redirect(f"/review/{review_id}") if review_id else redirect("/")

    if not reviews.get_review(review_id):
        abort(404)

    reviews.add_comment(review_id, session["user_id"], comment)
    return redirect(f"/review/{review_id}")

@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if not review:
        abort(404)

    if review["user_id"] != session["user_id"]:
        abort(403)

    all_classes = reviews.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in reviews.get_classes(review_id):
        classes[entry["title"]] = entry["value"]

    reviews.get_classes(review_id)
    return render_template("edit_review.html", review=review, all_classes=all_classes, classes=classes)


@app.route("/update_review", methods=["POST"])
def update_review():
    check_csrf()
    review_id = int(request.form["review_id"])
    review = reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    author = request.form["author"]
    review_text = request.form["review"]
    grade = request.form["grade"]

    try:
        grade = int(grade)
    except:
        flash("The grade must be an integer between 0 and 10")
        return redirect(f"/edit_review/{review_id}")

    if author and review_text and title and (grade or grade == 0):
        if len(title) > 100:
            flash(f"Book title is {len(title)-100} characters too long.")
            return redirect(f"/edit_review/{review_id}")
        if len(author) > 50:
            flash(f"Author name is {len(author)-50} characters too long.")
            return redirect(f"/edit_review/{review_id}")
        if not 10 >= int(grade) >= 0:
            flash("The grade must be between 0 and 10")
            return redirect(f"/edit_review/{review_id}")
    else:
        flash("All fields must be filled")
        return redirect(f"/edit_review/{review_id}")

    all_classes = reviews.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry and entry != "(select)" and ":" in entry:
            entry_title, entry_value = entry.split(":")
            if entry_title not in all_classes or entry_value not in all_classes[entry_title]:
                abort(403)
            classes.append((entry_title, entry_value))

    reviews.update_review(review_id, title, author, review_text, grade, classes)
    return redirect("/review/" + str(review_id))

@app.route("/delete_review/<int:review_id>", methods = ["GET", "POST"])
def delete_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if not review:
        abort(404)

    if review["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("delete_review.html", review=review)
    elif request.method == "POST":
        check_csrf()
        if "delete" in request.form:
            reviews.delete_review(review_id)
            return redirect("/")
        else: return redirect("/review/" + str(review_id))

@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment_route(comment_id):
    require_login()
    check_csrf()

    comment = reviews.get_comment(comment_id)
    if not comment:
        abort(404)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    review_id = comment["review_id"]
    reviews.delete_comment(comment_id)
    return redirect(f"/review/{review_id}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")
    check_csrf()
    username = request.form["username"]
    password = request.form["password"]
    if not username or not password:
        flash("Please fill in both username and password")
        return redirect("/login")

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    flash("Invalid username or password")
    return redirect("/login")


@app.route("/logout", methods=["POST"])
def logout():
    require_login()
    check_csrf()
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/new_review")
def review():
    require_login()
    classes = reviews.get_all_classes()
    return render_template("review.html", classes=classes)

@app.route("/new_comment")
def comment():
    require_login()
    classes = reviews.get_all_classes()
    return render_template("review.html", classes=classes)

@app.template_filter("convert_time")
def convert_time(value: str):
    t = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    t += timedelta(hours=3)
    return t.strftime("%-d.%-m.%Y %H:%M")

def check_csrf():
    token = request.form.get("csrf_token")
    session_token = session.get("csrf_token")
    if not token or not session_token or token != session_token:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)