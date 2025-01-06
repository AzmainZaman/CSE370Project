from flask import Blueprint, request, jsonify
from extensions import db
from models.models import User
import bcrypt

admin_bp = Blueprint('admin', __name__)

# Add a new user
@admin_bp.route('/add_user', methods=['POST'])
def add_user():
    """
    Adds a new user to the system.
    """
    data = request.json

    # Validate required fields
    required_fields = ['name', 'email', 'password', 'user_type']
    if not all(field in data for field in required_fields):
        return jsonify({"message": f"Missing required fields: {', '.join(required_fields)}"}), 400

    # Check for duplicate email
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Create a new user instance
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password.decode('utf-8'),
        user_type=data['user_type']
    )

    # Add the user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": f"User {new_user.name} added successfully!",
            "user": {
                "user_id": new_user.user_id,
                "name": new_user.name,
                "email": new_user.email,
                "user_type": new_user.user_type
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# View all users
@admin_bp.route('/view_users', methods=['GET'])
def view_users():
    """
    Retrieves a list of all users in the system.
    """
    users = User.query.all()
    user_list = [
        {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type
        }
        for user in users
    ]

    return jsonify({"users": user_list, "total_users": len(user_list)}), 200


# Update a user
@admin_bp.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates an existing user's details.
    """
    data = request.json
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Update user details if provided
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'password' in data and data['password']:
        user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.user_type = data.get('user_type', user.user_type)

    try:
        db.session.commit()
        return jsonify({
            "message": f"User {user.name} updated successfully!",
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# Delete a user
@admin_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user from the system.
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user.name} deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
