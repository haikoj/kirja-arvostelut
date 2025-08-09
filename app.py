import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import reviews
import users


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews = all_reviews)

@app.route("/find_review")
def find_review():
    query = request.args.get("query")
    if not query:
        query = " "
        results = []
    else:
        results = reviews.find_review(query)
    return render_template("find_review.html", query=query, results=results)

@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    if not review:
        abort(404)

    return render_template("show_review.html", review=review)


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Passwords do not match."
    if len(password1) < 4:
        return "Password must be at least 4 digits"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Username is already taken"

    return "Your account has been created!"


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    
    reviews = users.get_user_reviews(user_id)

    return render_template("show_user.html", user=user, reviews=reviews)

    
@app.route("/create_review", methods=["POST"])
def create_review():
    require_login()
    title = request.form["title"]
    review = request.form["review"]
    author = request.form["author"]
    grade = request.form["grade"]
    user_id = session["user_id"]

    try:
        grade = int(grade)
    except:
        return "The grade must be an integer between 0 and 10"


    if author and review and title and (grade or grade == 0):
        if len(title) > 100:
            return f"Book title is {len(title)-100} characters too long."
        if len(author) > 50:
            return f"Author name is {len(author)-50} characters too long."
        if 10 >= int(grade) >= 0:
            reviews.add_review(title, author, review, grade, user_id)
            return redirect("/")
        else:
            return "The grade must be between 0 and 10"
    else:
        return "All fields must be filled"


@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if not review:
        abort(404)

    if review["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_review.html", review=review)


@app.route("/update_review", methods=["POST"])
def update_review():
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
        return "The grade must be an integer between 0 and 10"


    if author and review and title and (grade or grade == 0):
        if len(title) > 100:
            return f"Book title is {len(title)-100} characters too long."
        if len(author) > 50:
            return f"Author name is {len(author)-50} characters too long."
        if 10 >= int(grade) >= 0:
            reviews.update_review(review_id, title, author, review_text, grade)
            return redirect("/review/" + str(review_id))
        else:
            return "The grade must be between 0 and 10"
    else:
        return "All fields must be filled"


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
        if "delete" in request.form:
            reviews.delete_review(review_id)
            return redirect("/")
        else: return redirect("/review/" + str(review_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return "Please fill in both username and password"

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "Invalid username or password"

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/new_review")
def review():
    require_login()
    return render_template("review.html")



def require_login():
    if "user_id" not in session:
        abort(403)