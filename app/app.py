from flask import Flask, request, jsonify, render_template
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_NAME = os.environ.get("DB_NAME", "tododb")


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def index():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, task FROM todos ORDER BY id DESC")
        todos = cur.fetchall()
    return render_template("index.html", todos=todos)


# ===== API ENDPOINTS =====

# Create a new task
@app.route("/api/todo", methods=["POST"])
def add_todo():
    data = request.get_json()
    task = data.get("task")

    if not task:
        return jsonify({"error": "Task is required"}), 400

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        conn.commit()
    return jsonify({"message": "Task added"}), 201


# Get all tasks
@app.route("/api/todo", methods=["GET"])
def get_todos():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, task FROM todos")
        items = cur.fetchall()
    return jsonify(items)


# Delete task
@app.route("/api/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
        conn.commit()
    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
