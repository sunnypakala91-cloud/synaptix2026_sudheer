from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# ------------------------
# Database create function
# ------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------------
# Home page
# ------------------------
@app.route('/')
def home():
    return render_template("index.html")


# ------------------------
# API: Submit score
# ------------------------
@app.route('/api/submit', methods=['POST'])
def submit_score():

    data = request.json

    name = data['name']
    score = data['score']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leaderboard (name, score) VALUES (?, ?)",
        (name, score)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Score saved"
    })


# ------------------------
# API: Get Top 10
# ------------------------
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, score
        FROM leaderboard
        ORDER BY score DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    leaderboard = []

    for row in rows:
        leaderboard.append({
            "name": row[0],
            "score": row[1]
        })

    return jsonify(leaderboard)


# ------------------------
# Run server
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)