from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
)
from models.models import Book, BookOrder
from extensions import db
from utils.decorators import role_required

librarian_bp = Blueprint('librarian', __name__)

# ------------------------------------
# 1) Protected route for the librarian dashboard
# ------------------------------------
@librarian_bp.route('/dashboard', methods=['GET'])
@jwt_required(locations=["cookies"])  
def librarian_dashboard():
    """
    This route requires a valid JWT in a cookie.
    If the user's role is not librarian, redirect them to login.
    """
    identity = get_jwt_identity()  # now safe to call
    if identity.get('role') != 'librarian':
        return redirect(url_for('auth.login_page'))
    return render_template('librarian_dashboard.html')


# ------------------------------------
# 2) Librarian-only routes for data manipulation
#    (EXAMPLE: switching these to cookie-based too)
# ------------------------------------

@librarian_bp.route('/add_book', methods=['POST'])
@jwt_required(locations=["cookies"])
# @role_required(['librarian', 'admin'])  
def add_book():
    data = request.json or {}
    if not all(key in data for key in ('title', 'author', 'genre', 'stock')):
        return jsonify({"message": "Missing required fields"}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        stock=data['stock'],
        location=data.get('location')  # optional
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": f"Book '{new_book.title}' added successfully!",
        "book": {
            "book_id": new_book.book_id,
            "title": new_book.title,
            "author": new_book.author,
            "genre": new_book.genre,
            "stock": new_book.stock,
            "location": new_book.location
        }
    }), 201


@librarian_bp.route('/view_books', methods=['GET'])
@jwt_required(locations=["cookies"])
def view_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)

    identity = get_jwt_identity()
    print(f"[DEBUG] /view_books called by user_id={identity.get('user_id')} with role={identity.get('role')}")

    book_list = [{
        "book_id": book.book_id,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "stock": book.stock,
        "location": book.location,
        "created_at": book.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for book in books.items]

    return jsonify({
        "books": book_list,
        "total": books.total,
        "pages": books.pages,
        "current_page": books.page
    })


@librarian_bp.route('/update_book/<int:book_id>', methods=['PUT'])
@jwt_required(locations=["cookies"])
# @role_required(['librarian', 'admin'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.json or {}
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.stock = data.get('stock', book.stock)
    book.location = data.get('location', book.location)

    db.session.commit()

    return jsonify({
        "message": f"Book '{book.title}' updated successfully!",
        "book": {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "stock": book.stock,
            "location": book.location
        }
    })


@librarian_bp.route('/delete_book/<int:book_id>', methods=['DELETE'])
@jwt_required(locations=["cookies"])
# @role_required(['librarian', 'admin'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": f"Book '{book.title}' deleted successfully!"})


@librarian_bp.route('/search_books', methods=['GET'])
@jwt_required(locations=["cookies"])
def search_books():
    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')

    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    books = query.all()
    book_list = [{
        "book_id": book.book_id,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "stock": book.stock,
        "location": book.location,
        "created_at": book.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for book in books]

    return jsonify({"books": book_list})


@librarian_bp.route('/order_books', methods=['POST'])
@jwt_required(locations=["cookies"])
# @role_required(['librarian', 'admin'])
def order_books():
    data = request.json or {}
    if not all(key in data for key in ('book_id', 'vendor_name', 'quantity', 'expected_delivery_date')):
        return jsonify({"message": "Missing required fields"}), 400

    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({"message": "Book not found"}), 404

    new_order = BookOrder(
        book_id=data['book_id'],
        vendor_name=data['vendor_name'],
        quantity=data['quantity'],
        expected_delivery_date=data['expected_delivery_date']
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "message": f"Order placed for {new_order.quantity} copies of '{book.title}' from {new_order.vendor_name}.",
        "order": {
            "order_id": new_order.order_id,
            "book_id": new_order.book_id,
            "vendor_name": new_order.vendor_name,
            "quantity": new_order.quantity,
            "expected_delivery_date": new_order.expected_delivery_date.strftime('%Y-%m-%d')
        }
    })


@librarian_bp.route('/view_orders', methods=['GET'])
@jwt_required(locations=["cookies"])
# @role_required(['librarian', 'admin'])
def view_orders():
    orders = BookOrder.query.all()
    order_list = [{
        "order_id": order.order_id,
        "book_title": order.book.title,
        "vendor_name": order.vendor_name,
        "quantity": order.quantity,
        "order_date": order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
        "expected_delivery_date": order.expected_delivery_date.strftime('%Y-%m-%d'),
        "order_status": order.order_status
    } for order in orders]

    return jsonify({"orders": order_list})
