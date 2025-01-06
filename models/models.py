from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    __tablename__ = 'USERS'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    user_type = db.Column(db.Enum('member', 'librarian', 'admin'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Hash the password before storing it
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Verify the password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Add user-friendly representation
    def __repr__(self):
        return f"<User {self.name} ({self.user_type})>"


class Book(db.Model):
    __tablename__ = 'BOOKS'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    location = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'stock': self.stock
        }

    # Add user-friendly representation
    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"


class BookOrder(db.Model):
    __tablename__ = 'BOOK_ORDERS'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('BOOKS.book_id'), nullable=False)
    vendor_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    expected_delivery_date = db.Column(db.Date, nullable=False)
    order_status = db.Column(db.String(50), default='Pending')

    # Relationship to the Book model
    book = db.relationship('Book', backref='orders')

    # Add user-friendly representation
    def __repr__(self):
        return f"<BookOrder {self.quantity}x {self.book.title} from {self.vendor_name}>"


class BorrowTransaction(db.Model):
    __tablename__ = 'BORROW_TRANSACTIONS'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('BOOKS.book_id'), nullable=False)
    borrow_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)

    # Relationships
    user = db.relationship('User', backref='borrow_transactions')
    book = db.relationship('Book', backref='borrow_transactions')

    # Add user-friendly representation
    def __repr__(self):
        return f"<BorrowTransaction User {self.user.name} borrowed {self.book.title}>"


class Fine(db.Model):
    __tablename__ = 'FINES'

    fine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('BORROW_TRANSACTIONS.transaction_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)

    # Relationship
    transaction = db.relationship('BorrowTransaction', backref='fine')

    # Add user-friendly representation
    def __repr__(self):
        return f"<Fine {self.amount} {'Paid' if self.paid else 'Unpaid'}>"
