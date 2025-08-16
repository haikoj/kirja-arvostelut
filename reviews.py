import db

def add_review(title, author, review, grade, user_id, classes):
    sql = """INSERT INTO items (title, author, review, grade, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, author, review, grade, user_id])

    review_id = db.last_insert_id()

    sql = """INSERT INTO review_classes (review_id, title, value)
             VALUES (?, ?, ?)"""
    for title2, value2 in classes:
        db.execute(sql, [review_id, title2, value2])


def get_reviews():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    
    return db.query(sql)

def get_classes(review_id):
    sql = """SELECT title, value FROM review_classes WHERE review_id = ?"""
    return db.query(sql, [review_id])

def get_all_classes():
    sql = """SELECT title, value FROM classes ORDER BY id"""
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_review(review_id):
    sql = """SELECT items.id, items.title, items.author, items.review, items.grade, users.username, users.id user_id
            FROM items, users
            WHERE items.user_id = users.id AND 
            items.id = ?"""
    
    result = db.query(sql, [review_id])
    if result:
        return result[0]
    else: return None

def update_review(review_id, title, author, review, grade):
    sql = """UPDATE items SET title = ?, author = ?, review = ?, grade = ?
            WHERE id = ?"""


    db.execute(sql, [title, author, review, grade, review_id])


def delete_review(review_id):
    sql = """DELETE FROM items WHERE id = ?"""
    db.execute(sql, [review_id])

def find_review(query):
    sql_base = "SELECT id, title FROM items WHERE"
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