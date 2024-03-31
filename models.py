# Import necessary modules and classes from Flask extensions
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()
# Initialize SQLAlchemy for database management
db = SQLAlchemy()

# Function to connect this database to the provided Flask app
def connect_db(app):
    """Connect this database to provided Flask app.
    
    You should call this in your Flask app.
    """
    # Set the Flask app for the database
    db.app = app
    # Initialize the database with the app
    db.init_app(app)

# Define User model for site users
class User(db.Model):
    """Site user."""
    # Define table name
    __tablename__ = "users"
    # Define columns for username, password, email, first name, and last name
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    # Define relationship with Feedback model
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
    # Define class methods for user registration and authentication
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""
        # Hash the password
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        # Create and add user to the session
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
        
        Return user if valid; else return False.
        """
        # Query user by username
        user = User.query.filter_by(username=username).first()
        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

# Define Feedback model for feedback entries
class Feedback(db.Model):
    """Feedback."""
    # Define table name
    __tablename__ = "feedback"
    # Define columns for id, title, content, and username
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
