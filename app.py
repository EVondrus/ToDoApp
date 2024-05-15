import os
from flask import Flask, render_template, request, redirect, url_for, g
from database import db, Todo

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))   # Get the directory of the this file
todo_file = os.path.join(basedir, 'todo_list.txt')     # Create the path to the to-do list file using the directory
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.before_request
def load_data_to_g():
    """
    Load the to-do items from the database and store them in the global variable 'g.todos'.

    Returns:
        None
    """
    todos = Todo.query.all()
    g.todos = todos
    g.todo = None
    

@app.route("/")
def index():
    """
    Renders the index.html template with the to-do list.

    Returns:
        The rendered HTML template with the to-do list.
    """
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_todo():
    """
    Adds a new to-do item to the list.

    Function is responsible for adding a new to-do item to the list. It retrieves the name of the to-do item from the request form data and creates a new `Todo` object with the given name. The new to-do item is then added to the database session and committed.

    Returns:
        Redirects to the index page after adding the to-do item.
    """
    todo = Todo(name=request.form["todo"])
    # add the new ToDo to the list
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/remove/<int:id>", methods=["GET", "POST"])
def remove_todo(id):
    """
    Removes a to-do item from the list.

    Function is responsible for removing a to-do item from the list. 
    It retrieves the id of the to-do item from the URL parameter 
    and deletes the corresponding `Todo` object from the database session.
    
    Returns:
        Redirects to the index page after removing the to-do item.
    """
    db.session.delete(Todo.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)