from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Category, Expense
from datetime import datetime, timedelta

controller_bp = Blueprint('controller', __name__)

# User Registration
@controller_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    new_user.set_name(name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User Login
@controller_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    return jsonify(access_token=access_token,name = user.username), 200

# Get All Users
@controller_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username
        })
    return jsonify(user_list), 200

# Add Expense Category
@controller_bp.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    new_category = Category(
        name=data.get('name'),
        description=data.get('description', ''),
        image_url=data.get('image_url', '')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({
        "id": new_category.id,
        "name": new_category.name,
        "description": new_category.description,
        "image_url": new_category.image_url
    }), 201

# Get All Categories
@controller_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    category_list = []
    for category in categories:
        category_list.append({
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "image_url": category.image_url
        })
    return jsonify(category_list), 200
# Delete Category
@controller_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({
            "message": "Category deleted successfully",
            "category": {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "image_url": category.image_url
            }
        }), 200
    return jsonify({"error": "Category not found"}), 404

# Add Expense
@controller_bp.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    category = Category.query.get(data.get('category_id'))
    if not category:
        return jsonify({"error": "Category not found"}), 400

    new_expense = Expense(
        amount=data.get('amount'),
        category_id=data.get('category_id'),
        description=data.get('description', ''),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({
        "id": new_expense.id,
        "amount": new_expense.amount,
        "category_id": new_expense.category_id,
        "description": new_expense.description,
        "date": new_expense.date.isoformat(),
        "category_image_url": category.image_url,
        "is_deleted": new_expense.is_deleted
    }), 201

# Get All Expenses
@controller_bp.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    expenses = Expense.query.filter_by(is_deleted=False).all()
    expense_list = []
    for expense in expenses:
        expense_list.append({
            "id": expense.id,
            "amount": expense.amount,
            "category_id": expense.category_id,
            "description": expense.description,
            "date": expense.date.isoformat(),
            "category_image_url": expense.category.image_url,
            "is_deleted": expense.is_deleted
        })
    return jsonify(expense_list), 200

# Delete Expense
@controller_bp.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        expense.is_deleted = True
        db.session.commit()
        return jsonify({
            "message": "Expense deleted successfully",
            "expense": {
                "id": expense.id,
                "amount": expense.amount,
                "category_id": expense.category_id,
                "description": expense.description,
                "date": expense.date.isoformat(),
                "is_deleted": expense.is_deleted
            }
        }), 200
    return jsonify({"error": "Expense not found"}), 404

# Get Deleted Expenses
@controller_bp.route('/expenses/deleted', methods=['GET'])
@jwt_required()
def get_deleted_expenses():
    deleted_expenses = Expense.query.filter_by(is_deleted=True).all()
    deleted_list = []
    for expense in deleted_expenses:
        deleted_list.append({
            "id": expense.id,
            "amount": expense.amount,
            "category_id": expense.category_id,
            "description": expense.description,
            "date": expense.date.isoformat(),
            "category_image_url": expense.category.image_url,
            "is_deleted": expense.is_deleted
        })
    return jsonify(deleted_list), 200
