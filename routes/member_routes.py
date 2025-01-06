from flask import Blueprint, jsonify, request
from models.models import db, Member, BorrowedBook, User, Book

main = Blueprint('main', __name__)

@main.route('/members', methods=['GET'])
def get_members():
    try:
        members = Member.query.join(User, Member.user_id == User.user_id).all()
        return jsonify([{"id": m.member_id, "name": m.user.name, "email": m.user.email} for m in members])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/members/register', methods=['POST'])
def register_member():
    data = request.json
    try:
        # Validate input data
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the email is already registered
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 409

        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # Hash this in production
            user_type='member'
        )
        db.session.add(new_user)
        db.session.flush()  # Get the new user's ID without committing

        # Create new member
        new_member = Member(
            user_id=new_user.user_id,
            membership_date=data.get('registration_date', None),
            status='active'
        )
        db.session.add(new_member)
        db.session.commit()

        return jsonify({"message": "Member registered successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/test-db', methods=['GET'])
def test_db():
    print("Reached /test-db")  # Debug message to ensure route is reached
    try:
        with db.engine.connect() as connection:
            result = connection.execute(db.text("SELECT DATABASE();"))
            db_name = [row[0] for row in result]
            return jsonify({"message": "Connected!", "database": db_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/search-books', methods=['GET'])
def search_books():
    query = request.args.get('query', '').lower()
    try:
        books = Book.query.filter(
            (Book.title.ilike(f"%{query}%")) | 
            (Book.author.ilike(f"%{query}%")) | 
            (Book.genre.ilike(f"%{query}%"))
        ).all()
        return jsonify([{
            "id": book.book_id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "copies_available": book.copies_available
        } for book in books]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/borrow-book', methods=['POST'])
def borrow_book():
    data = request.json
    try:
        member_id = data.get('member_id')
        book_id = data.get('book_id')
        borrow_date = data.get('borrow_date') 
        due_date = data.get('due_date')

        # Check if the book is available
        book = Book.query.get(book_id)
        if not book or book.copies_available < 1:
            return jsonify({"error": "Book is not available"}), 400

        # Create a new borrowed book entry
        borrowed_book = BorrowedBook(
            user_id=member_id,
            book_id=book_id,
            borrow_date=borrow_date,
            due_date=due_date
        )
        db.session.add(borrowed_book)

        # Update book availability
        book.copies_available -= 1
        db.session.commit()

        return jsonify({"message": "Book borrowed successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/borrowed-books/<int:member_id>', methods=['GET'])
def view_borrowed_books(member_id):
    try:
        borrowed_books = BorrowedBook.query.filter_by(user_id=member_id).all()
        return jsonify([{
            "borrow_id": b.borrow_id,
            "book_title": b.book.title,
            "borrow_date": b.borrow_date,
            "due_date": b.due_date,
            "return_date": b.return_date
        } for b in borrowed_books]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




