from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
from models.models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

# ------------------------------------------------
# 1) Serve the login page
# ------------------------------------------------
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html') 

# ------------------------------------------------
# 2) Login route (sets JWT in a cookie and redirects based on role)
# ------------------------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login by validating credentials and returning a cookie-based JWT.
    """
    data = request.json

    # Validate required fields
    if not all(key in data for key in ('email', 'password')):
        return jsonify({"message": "Missing email or password", "success": False}), 400

    # Find the user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid email or password", "success": False}), 401

    # Create a JWT token. The identity includes role & user_id
    access_token = create_access_token(identity={"user_id": user.user_id, "role": user.user_type})

    # Build the JSON response
    resp = jsonify({
        "message": "Login successful",
        "success": True,
        "role": user.user_type
        # We no longer return "access_token" in JSON 
        # since we're setting it in a cookie
    })

    # Set the JWT cookie
    set_access_cookies(resp, access_token)

    # # Role-based redirection logic
    # if user.user_type == 'admin':
    #     return redirect(url_for('admin.dashboard'))  # Example admin dashboard route
    # elif user.user_type == 'librarian':
    #     return redirect(url_for('librarian.dashboard'))  # Example librarian dashboard route
    # elif user.user_type == 'member':
    #     return redirect(url_for('member.dashboard'))  # Example member dashboard route

    return resp, 200

# ------------------------------------------------
# 3) Logout route (clears the JWT cookie)
# ------------------------------------------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logs out the user by clearing the JWT cookies.
    """
    resp = jsonify({"message": "Logged out successfully", "success": True})
    unset_jwt_cookies(resp)   # This clears the JWT cookies
    return resp, 200

# ------------------------------------------------
# 4) Current user route (requires JWT in cookie)
# ------------------------------------------------
@auth_bp.route('/current_user', methods=['GET'])
@jwt_required(locations=["cookies"])
def current_user():
    """
    Retrieves the currently logged-in user's details using the JWT token in the cookie.
    """
    identity = get_jwt_identity()
    user = User.query.get(identity['user_id'])

    if not user:
        return jsonify({"message": "User not found", "success": False}), 404

    return jsonify({
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type
        },
        "success": True
    })

# ------------------------------------------------
# 5) Register route (still open, no JWT needed)
# ------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user by creating a database entry.
    """
    data = request.json

    # Validate required fields
    if not all(key in data for key in ('name', 'email', 'password')):
        return jsonify({"message": "Missing required fields", "success": False}), 400

    # Enforce role assignment
    user_type = 'member'

    # Check if the email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered", "success": False}), 400

    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        user_type=user_type
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "success": True}), 201
