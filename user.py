from flask import Blueprint, jsonify, request, session
from src.models.user import User, db
from functools import wraps

user_bp = Blueprint('user', __name__)

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'user_type', 'full_name']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Validate user type
    if data['user_type'] not in ['employer', 'job_seeker']:
        return jsonify({'error': 'Invalid user type'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        user_type=data['user_type'],
        full_name=data['full_name'],
        phone=data.get('phone'),
        company_name=data.get('company_name') if data['user_type'] == 'employer' else None
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        session['user_type'] = user.user_type
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    user = User.query.get(session['user_id'])
    return jsonify(user.to_dict())

@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update current user profile"""
    user = User.query.get(session['user_id'])
    data = request.json
    
    # Update allowed fields
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    
    if user.user_type == 'employer':
        user.company_name = data.get('company_name', user.company_name)
    
    # Check if email is already taken by another user
    if data.get('email') and data['email'] != user.email:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully', 'user': user.to_dict()})

@user_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deleting themselves
    if user.id == session['user_id']:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
