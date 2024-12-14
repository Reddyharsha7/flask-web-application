from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask To-Do List</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        form { margin-bottom: 20px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        .delete-btn { color: red; cursor: pointer; }
    </style>
</head>
<body>
    <h1>To-Do List</h1>
    <form action="/add" method="POST">
        <input type="text" name="title" placeholder="Enter a new task" required>
        <button type="submit">Add Task</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>
                {{ task.title }}
                <a href="/delete/{{ task.id }}" class="delete-btn">[Delete]</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form['title']
    new_task = Task(title=task_title)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
