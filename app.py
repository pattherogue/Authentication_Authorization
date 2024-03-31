# Import necessary modules and classes from Flask and project files
from flask import Flask, render_template, redirect, session

from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback  # Importing models from project files
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm  # Importing forms from project files

# Create Flask app instance
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback"  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoiding excessive database tracking
app.config['SQLALCHEMY_ECHO'] = True  # Echo SQL queries to console for debugging
app.config['SECRET_KEY'] = "shhhhh"  # Secret key for session management
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Debug toolbar configuration

# Enable DebugToolbarExtension for debugging


# Connect to the database
connect_db(app)

# Route for the homepage, redirects to register page
@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""
    return redirect("/register")

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""
    # Redirect if user is already logged in
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    # Create registration form
    form = RegisterForm()
    # Handle form submission
    if form.validate_on_submit():
        # Extract form data
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        # Register user
        user = User.register(username, password, first_name, last_name, email)
        db.session.commit()
        session['username'] = user.username
        return redirect(f"/users/{user.username}")
    else:
        return render_template("users/register.html", form=form)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""
    # Redirect if user is already logged in
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    # Create login form
    form = LoginForm()
    # Handle form submission
    if form.validate_on_submit():
        # Extract form data
        username = form.username.data
        password = form.password.data
        # Authenticate user
        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)
    return render_template("users/login.html", form=form)

# Route for user logout
@app.route("/logout")
def logout():
    """Logout route."""
    session.pop("username")
    return redirect("/login")

# Route to display user profile
@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    form = DeleteForm()
    return render_template("users/show.html", user=user, form=form)

# Route to delete user profile
@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")

# Route to add new feedback
@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/new.html", form=form)

# Route to update existing feedback
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

# Route to delete feedback
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{feedback.username}")
