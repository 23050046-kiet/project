from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Desk, UserCardProgress
from sqlalchemy import func
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads/desks'

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bạn không có quyền truy cập', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.asc()).paginate(page=page, per_page=10)
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/desks', methods=['GET'])
@login_required
@admin_required
def desks_index():
    """List all desks"""
    page = request.args.get('page', 1, type=int)
    desks = Desk.query.order_by(Desk.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/desks/index.html', desks=desks)

@admin_bp.route('/desks/create', methods=['GET'])
@login_required
@admin_required
def desks_create():
    """Show create desk form"""
    return render_template('admin/desks/create.html')

@admin_bp.route('/desks', methods=['POST'])
@login_required
@admin_required
def desks_store():
    """Store new desk"""
    name_en = request.form.get('name_en', '').strip()
    image = request.files.get('image')
    
    # Validation
    if not name_en:
        flash('Tên không được để trống', 'error')
        return redirect(url_for('admin.desks_create'))
    
    if len(name_en) > 255:
        flash('Tên không được quá 255 ký tự', 'error')
        return redirect(url_for('admin.desks_create'))
    
    if not image or image.filename == '':
        flash('Vui lòng chọn ảnh', 'error')
        return redirect(url_for('admin.desks_create'))
    
    if not allowed_file(image.filename):
        flash('Chỉ chấp nhận file ảnh (PNG, JPG, JPEG, GIF)', 'error')
        return redirect(url_for('admin.desks_create'))
    
    # Create uploads folder if not exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Save image
    filename = secure_filename(image.filename)
    # Add timestamp to filename to avoid conflicts
    import time
    filename = f"{int(time.time())}_{filename}"
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)
    
    # Create desk record
    desk = Desk(
        name_en=name_en,
        image_path=f"desks/{filename}"
    )
    
    db.session.add(desk)
    db.session.commit()
    
    flash('Tạo card thành công!', 'success')
    return redirect(url_for('admin.desks_index'))

@admin_bp.route('/desks/<int:desk_id>', methods=['DELETE'])
@login_required
@admin_required
def desks_destroy(desk_id):
    """Delete desk"""
    desk = Desk.query.get(desk_id)
    
    if not desk:
        return jsonify({'error': 'Desk not found'}), 404
    
    # Delete image if exists
    if desk.image_path:
        image_path = os.path.join('uploads', desk.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(desk)
    db.session.commit()
    
    flash('Xóa card thành công!', 'success')
    return redirect(url_for('admin.desks_index'))

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def users_destroy(user_id):
    """Delete user"""
    user = User.query.get(user_id)
    
    if not user:
        flash('User không tồn tại', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if user.id == current_user.id:
        flash('Không thể xóa tài khoản của chính bạn.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Xóa user thành công!', 'success')
    return redirect(url_for('admin.dashboard'))
