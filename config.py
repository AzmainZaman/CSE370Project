import os
import jwt

class Config:
    SECRET_KEY = 'a-very-secure-and-long-secret-key-1234567890'
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/lms_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = 'a-very-secure-and-long-secret-key-1234567890'
    
    # -----------------------------
    # Cookie-based JWT config
    # -----------------------------
    JWT_TOKEN_LOCATION = ["cookies"]  # So Flask-JWT-Extended looks for tokens in cookies
    JWT_COOKIE_SECURE = False         # Set to True if your site is HTTPS only
    JWT_COOKIE_SAMESITE = "Lax"       # Could be 'None', 'Lax', or 'Strict'
    JWT_COOKIE_CSRF_PROTECT = False   # Set to True if you want CSRF protection
