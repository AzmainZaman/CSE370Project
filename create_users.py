# from werkzeug.security import generate_password_hash
# from models.models import User
# from extensions import db
# from flask import Flask
# from config import Config

# # Initialize Flask app and database
# app = Flask(__name__)
# app.config.from_object(Config)
# db.init_app(app)

# def create_user(name, email, password, user_type):
#     """
#     Creates a new user with hashed password and adds to the database.
#     """
#     with app.app_context():
#         # Check if user already exists
#         if User.query.filter_by(email=email).first():
#             print(f"User with email {email} already exists.")
#             return

#         # Create new user
#         hashed_password = generate_password_hash(password)
#         new_user = User(name=name, email=email, password=hashed_password, user_type=user_type)

#         # Add to the database
#         db.session.add(new_user)
#         db.session.commit()

#         print(f"User '{name}' added successfully!")

# # Example Usage
# if __name__ == "__main__":
#     # Create users
#     create_user(name="Admin User", email="admin@example.com", password="admin123", user_type="admin")
#     create_user(name="Librarian User", email="librarian@example.com", password="librarian123", user_type="librarian")
#     create_user(name="Member User", email="member@example.com", password="member123", user_type="member")
