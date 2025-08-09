import db

def get_user(user_id):
    sql = """SELECT id, username
            FROM users
            WHERE id = ?"""
    
    result = db.query(sql, [user_id])
    
    if result:
        return result[0]
    else: return None

def get_user_reviews(user_id):
    sql = """SELECT id, title, author 
            FROM items
            WHERE user_id = ?
            ORDER BY id DESC"""

    return db.query(sql, [user_id])