from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from db import (
    create_task,
    get_all_tasks,
    get_task,
    mark_completed,
    delete_task
)

app = Flask(__name__)
CORS(app)


def task_to_dict(task):
    if not task:
        return None
    task_id, title, description, completed, created_at = task
    return {
        'id': task_id,
        'title': title,
        'description': description,
        'completed': completed,
        'created_at': created_at.isoformat() if created_at else None,
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = get_all_tasks()
    return jsonify([task_to_dict(t) for t in tasks])

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task_to_dict(task))

@app.route("/tasks", methods=["POST"])
def create():
    data = request.json or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    task_id = create_task(title, description)
    task = get_task(task_id)
    return jsonify(task_to_dict(task)), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def complete(task_id):
    task = get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    mark_completed(task_id)
    task = get_task(task_id)
    return jsonify(task_to_dict(task)), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete(task_id):
    task = get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    delete_task(task_id)
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)

