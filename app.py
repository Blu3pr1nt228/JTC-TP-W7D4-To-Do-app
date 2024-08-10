# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Load user for login management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route to display all todos
@app.route('/')
@login_required
def show_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()  # Fetch todos for the current user
    return render_template('index.html', todos=todos)  # Render the todos on the index page

# Route to add a new todo
@app.route('/add', methods=['POST'])
@login_required
def add_todo():
    content = request.form['content']  # Get the todo content from the form
    new_todo = Todo(content=content, user_id=current_user.id)  # Create a new Todo item
    db.session.add(new_todo)  # Add the new Todo to the database
    db.session.commit()  # Commit the transaction
    return redirect(url_for('show_todos'))  # Redirect back to the todos page

# Route to toggle todo completion status
@app.route('/toggle/<int:id>')
@login_required
def toggle_complete(id):
    todo = Todo.query.get(id)  # Get the Todo item by ID
    todo.completed = not todo.completed  # Toggle the completion status
    db.session.commit()  # Commit the transaction
    return redirect(url_for('show_todos'))  # Redirect back to the todos page

# Route to delete a todo
@app.route('/delete/<int:id>')
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)  # Get the Todo item by ID
    db.session.delete(todo)  # Delete the Todo item
    db.session.commit()  # Commit the transaction
    return redirect(url_for('show_todos'))  # Redirect

