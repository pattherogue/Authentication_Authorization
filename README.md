# User Feedback Management Application

## Overview

This project is a Flask-based web application developed with Python, enabling users to register, log in, and manage their feedback entries. Leveraging Python's Flask framework, the application provides an intuitive interface for users to submit feedback, view their feedback, and manage their profiles.

## Project Structure

- **`app.py`**: The core application file, setting up routes, database integration, and application configuration.
- **`forms.py`**: Defines form classes (`RegisterForm`, `LoginForm`, `FeedbackForm`, etc.) for handling user input.
- **`models.py`**: Contains SQLAlchemy models (`User`, `Feedback`) that define the structure of the database.
- **`requirements.txt`**: Lists the required Python packages to run the application.
- **`seed.sql`**: SQL script to set up the initial database schema.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- PostgreSQL (or another supported database)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   psql -f seed.sql
   ```

4. Set the environment variable for the database URI (optional, defaults to local PostgreSQL):
   ```bash
   export DATABASE_URL=postgresql:///feedback_exercise
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application in your web browser at `http://127.0.0.1:5000`.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.
