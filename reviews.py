import db

def add_review(title, author, review, grade, user_id):
    sql = """INSERT INTO items (title, author, review, grade, user_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, author, review, grade, user_id])

def get_reviews():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    
    return db.query(sql)

def get_review(review_id):
    sql = """SELECT items.title, items.author, items.review, items.grade, users.username
            FROM items, users
            WHERE items.user_id = users.id AND 
            items.id = ?"""
    
    return db.query(sql, [review_id])[0]