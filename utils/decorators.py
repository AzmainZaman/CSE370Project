from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                # Verify JWT
                verify_jwt_in_request()
                claims = get_jwt()

                # Check if the role matches
                user_type = claims.get("user_type")
                if user_type not in required_roles:
                    return jsonify({"message": "Access forbidden: Unauthorized role"}), 403

                return fn(*args, **kwargs)
            except KeyError as e:
                return jsonify({"message": f"Missing key in JWT claims: {str(e)}"}), 400
            except Exception as e:
                return jsonify({"message": f"Authorization error: {str(e)}"}), 401
        return decorator
    return wrapper
