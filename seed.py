import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM comments")
db.execute("DELETE FROM review_classes")
db.execute("DELETE FROM reviews")
db.execute("DELETE FROM users")

user_count = 1000
review_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
                ["user" + str(i)])

for i in range(1, review_count + 1):
    random_user_id = random.randint(1, user_count)
    db.execute(
        """INSERT INTO reviews (title, author, review, grade, user_id) 
        VALUES (?, ?, ?, ?, ?)""",
        ["review" + str(i), "review" + str(i), "review" + str(i), 1, random_user_id],
    )

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    review_id = random.randint(1, review_count)
    db.execute(
        """INSERT INTO comments (review_id, user_id, comment) 
        VALUES (?, ?, ?)""",
        [review_id, user_id, "comment" + str(i)],
    )

db.commit()
db.close()
