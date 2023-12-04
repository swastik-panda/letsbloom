from pymongo import MongoClient

@app.route("/api/books", methods=["GET"])
def get_all_books():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["library"]
        books_collection = db["books"]

        # Use cursor to iterate over books
        cursor = books_collection.find({})

        # Stream data as JSON
        return jsonify([book for book in cursor])
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

from flask import request
from flask_sqlalchemy import SQLAlchemy

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    # ... other fields

@app.route("/api/books", methods=["GET"])
def get_all_books():
    try:
        # Get page number from query parameter
        page = int(request.args.get("page", 1))

        # Pagination logic
        books = Book.query.paginate(page=page, per_page=10)

        # Return paginated data
        return jsonify({"books": [book.serialize() for book in books.items],
                       "total_pages": books.pages})
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

