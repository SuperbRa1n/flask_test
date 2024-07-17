from flask import Blueprint, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Message

bp = Blueprint('main', __name__)

@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first() or User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 400
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@bp.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    message = Message(content=data['content'], user_id=current_user.id)
    db.session.add(message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'}), 201

@bp.route('/api/messages', methods=['GET'])
@login_required
def get_messages():
    # 获取所有用户发送的所有消息
    messages = Message.query.all()
    return jsonify([{'content': msg.content, 'date_posted': msg.date_posted, 'sender': User.query.filter_by(id=msg.user_id).first().username} for msg in messages]), 200

@bp.route('/api/admin/users', methods=['GET'])
@login_required
def admin_get_users():
    if current_user.username != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    users = User.query.all()
    return jsonify([{'username': user.username, 'email': user.email} for user in users]), 200
