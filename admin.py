from flask import Blueprint, jsonify, request, session
from src.models.user import User, Job, Application, db
from src.routes.user import admin_required
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics for admin"""
    
    # Count statistics
    total_users = User.query.count()
    total_employers = User.query.filter_by(user_type='employer').count()
    total_job_seekers = User.query.filter_by(user_type='job_seeker').count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_applications = Application.query.count()
    
    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(5).all()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_employers': total_employers,
            'total_job_seekers': total_job_seekers,
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'total_applications': total_applications
        },
        'recent_activity': {
            'users': [user.to_dict() for user in recent_users],
            'jobs': [job.to_dict() for job in recent_jobs],
            'applications': [app.to_dict() for app in recent_applications]
        }
    })

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with pagination and filtering"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    user_type = request.args.get('user_type', '')
    search = request.args.get('search', '')
    
    query = User.query
    
    # Apply filters
    if user_type:
        query = query.filter_by(user_type=user_type)
    
    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.email.contains(search)) |
            (User.full_name.contains(search))
        )
    
    # Order by creation date
    query = query.order_by(User.created_at.desc())
    
    # Paginate results
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page,
        'per_page': per_page
    })

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
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

@admin_bp.route('/jobs', methods=['GET'])
@admin_required
def get_all_jobs():
    """Get all jobs with pagination and filtering"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    status = request.args.get('status', '')  # 'active' or 'inactive'
    search = request.args.get('search', '')
    
    query = Job.query
    
    # Apply filters
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    if search:
        query = query.filter(
            (Job.title.contains(search)) |
            (Job.description.contains(search)) |
            (Job.location.contains(search))
        )
    
    # Order by creation date
    query = query.order_by(Job.created_at.desc())
    
    # Paginate results
    jobs = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'jobs': [job.to_dict() for job in jobs.items],
        'total': jobs.total,
        'pages': jobs.pages,
        'current_page': page,
        'per_page': per_page
    })

@admin_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@admin_required
def delete_job(job_id):
    """Delete a job posting (admin only)"""
    job = Job.query.get_or_404(job_id)
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message': 'Job deleted successfully'}), 200

@admin_bp.route('/jobs/<int:job_id>/toggle-status', methods=['PUT'])
@admin_required
def toggle_job_status(job_id):
    """Toggle job active status (admin only)"""
    job = Job.query.get_or_404(job_id)
    
    job.is_active = not job.is_active
    db.session.commit()
    
    status = 'activated' if job.is_active else 'deactivated'
    return jsonify({'message': f'Job {status} successfully', 'job': job.to_dict()})

@admin_bp.route('/applications', methods=['GET'])
@admin_required
def get_all_applications():
    """Get all applications with pagination and filtering"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    status = request.args.get('status', '')
    
    query = Application.query
    
    # Apply filters
    if status:
        query = query.filter_by(status=status)
    
    # Order by application date
    query = query.order_by(Application.applied_at.desc())
    
    # Paginate results
    applications = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'applications': [app.to_dict() for app in applications.items],
        'total': applications.total,
        'pages': applications.pages,
        'current_page': page,
        'per_page': per_page
    })

@admin_bp.route('/applications/<int:application_id>', methods=['DELETE'])
@admin_required
def delete_application(application_id):
    """Delete an application (admin only)"""
    application = Application.query.get_or_404(application_id)
    
    db.session.delete(application)
    db.session.commit()
    
    return jsonify({'message': 'Application deleted successfully'}), 200

