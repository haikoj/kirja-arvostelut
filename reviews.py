import db

def add_review(title, author, review, grade, user_id, classes):
    sql = """INSERT INTO reviews (title, author, review, grade, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, author, review, grade, user_id])

    review_id = db.last_insert_id()

    sql = """INSERT INTO review_classes (review_id, title, value)
             VALUES (?, ?, ?)"""
    for title2, value2 in classes:
        db.execute(sql, [review_id, title2, value2])

def add_comment(review_id, user_id, comment):
    sql = """INSERT INTO comments (review_id, user_id, comment)
            VALUES (?, ?, ?)"""
    db.execute(sql, [review_id, user_id, comment])

def get_reviews():
    sql = """SELECT r.id, r.title, r.author, u.username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            ORDER BY r.id DESC"""
    
    return db.query(sql)

def get_comments(review_id):
    sql = """SELECT c.comment, c.comment_time, c.id comment_id, c.user_id user_id, c.review_id review_id, u.username
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.review_id = ?
            ORDER BY c.id"""

    return db.query(sql, [review_id])

def get_classes(review_id):
    sql = """SELECT title, value FROM review_classes WHERE review_id = ?"""
    return db.query(sql, [review_id])

def get_all_classes():
    sql = """SELECT title, value FROM classes ORDER BY id"""
    result = db.query(sql)

    classes = {}

    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes

def get_comment(comment_id):
    sql = """SELECT id, review_id, user_id, comment, comment_time
            FROM comments
            WHERE id = ?"""
    result = db.query(sql, [comment_id])
    if result:
        return result[0]
    else: return None

def get_review(review_id):
    sql = """SELECT reviews.id, reviews.title, reviews.author, reviews.review, reviews.grade,
            reviews.review_time, reviews.edit_time,
            users.username, users.id user_id
            FROM reviews, users
            WHERE reviews.user_id = users.id AND 
            reviews.id = ?"""
    
    result = db.query(sql, [review_id])
    if result:
        return result[0]
    else: return None


def update_review(review_id, book_title, author, review, grade, classes):
    sql = """DELETE FROM review_classes
            WHERE review_id = ?"""
    db.execute(sql, [review_id])

    sql = """INSERT INTO review_classes (review_id, title, value)
             VALUES (?, ?, ?)"""
    for title, value in classes:
        db.execute(sql, [review_id, title, value])

    sql = """UPDATE reviews
            SET title = ?, author = ?, review = ?, grade = ?, edit_time = CURRENT_TIMESTAMP
            WHERE id = ?"""
    db.execute(sql, [book_title, author, review, grade, review_id])


def delete_review(review_id):
    sql = """DELETE FROM comments WHERE review_id = ?"""
    db.execute(sql, [review_id])

    sql = """DELETE FROM review_classes WHERE review_id = ?"""
    db.execute(sql, [review_id])

    sql = """DELETE FROM reviews WHERE id = ?"""
    db.execute(sql, [review_id])

def delete_comment(comment_id):
    sql = """DELETE FROM comments WHERE id = ?"""
    db.execute(sql, [comment_id])

def find_review(query):
    sql_base = "SELECT id, title FROM reviews WHERE"
    words = query.strip().split()
    possible = []
    separate_words = []

    for word in words:
        like = f"%{word}%"
        possible.append("title LIKE ?")
        possible.append("author LIKE ?")
        separate_words.extend([like, like])

    sql = f"{sql_base} {' OR '.join(possible)} ORDER BY id DESC"
    return db.query(sql, separate_words)