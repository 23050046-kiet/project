from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def guest_required(f):
    """Decorator to require guest (not logged in)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
@guest_required
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Email và mật khẩu không được để trống', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Thông tin đăng nhập không đúng', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        
        if user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@guest_required
def register():
    """Handle user registration"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirmation = request.form.get('password_confirmation', '')
        
        # Validation
        errors = []
        if not name:
            errors.append('Tên không được để trống')
        if not email:
            errors.append('Email không được để trống')
        if len(email) > 255:
            errors.append('Email không được quá 255 ký tự')
        if '@' not in email:
            errors.append('Email không hợp lệ')
        if User.query.filter_by(email=email).first():
            errors.append('Email đã được đăng ký')
        if not password:
            errors.append('Mật khẩu không được để trống')
        if len(password) < 6:
            errors.append('Mật khẩu phải có ít nhất 6 ký tự')
        if password != password_confirmation:
            errors.append('Xác nhận mật khẩu không trùng khớp')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(name=name, email=email, is_admin=False)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('Đã đăng xuất!', 'success')
    return redirect(url_for('auth.login'))
