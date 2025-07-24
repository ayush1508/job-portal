from flask import Blueprint, jsonify, request, session
from src.models.user import User, Job, Application, db
from src.routes.user import login_required
from sqlalchemy import or_

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Get all active jobs with optional search and filter"""
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    query = Job.query.filter_by(is_active=True)
    
    # Apply search filters
    if search:
        query = query.filter(or_(
            Job.title.contains(search),
            Job.description.contains(search),
            Job.requirements.contains(search)
        ))
    
    if location:
        query = query.filter(Job.location.contains(location))
    
    # Order by creation date (newest first)
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

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job by ID"""
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@jobs_bp.route('/jobs', methods=['POST'])
@login_required
def create_job():
    """Create a new job posting (employers only)"""
    user = User.query.get(session['user_id'])
    
    if user.user_type != 'employer':
        return jsonify({'error': 'Only employers can post jobs'}), 403
    
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'description', 'location']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Create new job
    job = Job(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        salary=data.get('salary'),
        requirements=data.get('requirements'),
        employer_id=user.id
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({'message': 'Job posted successfully', 'job': job.to_dict()}), 201

@jobs_bp.route('/jobs/<int:job_id>', methods=['PUT'])
@login_required
def update_job(job_id):
    """Update a job posting (job owner only)"""
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])
    
    # Check if user owns this job or is admin
    if job.employer_id != user.id and user.user_type != 'admin':
        return jsonify({'error': 'You can only edit your own job postings'}), 403
    
    data = request.json
    
    # Update job fields
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.location = data.get('location', job.location)
    job.salary = data.get('salary', job.salary)
    job.requirements = data.get('requirements', job.requirements)
    job.is_active = data.get('is_active', job.is_active)
    
    db.session.commit()
    
    return jsonify({'message': 'Job updated successfully', 'job': job.to_dict()})

@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@login_required
def delete_job(job_id):
    """Delete a job posting (job owner or admin only)"""
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])
    
    # Check if user owns this job or is admin
    if job.employer_id != user.id and user.user_type != 'admin':
        return jsonify({'error': 'You can only delete your own job postings'}), 403
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message': 'Job deleted successfully'}), 200

@jobs_bp.route('/my-jobs', methods=['GET'])
@login_required
def get_my_jobs():
    """Get jobs posted by current employer"""
    user = User.query.get(session['user_id'])
    
    if user.user_type != 'employer':
        return jsonify({'error': 'Only employers can view their job postings'}), 403
    
    jobs = Job.query.filter_by(employer_id=user.id).order_by(Job.created_at.desc()).all()
    
    return jsonify([job.to_dict() for job in jobs])

@jobs_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@login_required
def get_job_applications(job_id):
    """Get applications for a specific job (job owner only)"""
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])
    
    # Check if user owns this job or is admin
    if job.employer_id != user.id and user.user_type != 'admin':
        return jsonify({'error': 'You can only view applications for your own jobs'}), 403
    
    applications = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
    
    return jsonify([app.to_dict() for app in applications])

@jobs_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@login_required
def apply_to_job(job_id):
    """Apply to a job (job seekers only)"""
    user = User.query.get(session['user_id'])
    
    if user.user_type != 'job_seeker':
        return jsonify({'error': 'Only job seekers can apply to jobs'}), 403
    
    job = Job.query.get_or_404(job_id)
    
    if not job.is_active:
        return jsonify({'error': 'This job is no longer active'}), 400
    
    # Check if user has already applied
    existing_application = Application.query.filter_by(job_id=job_id, applicant_id=user.id).first()
    if existing_application:
        return jsonify({'error': 'You have already applied to this job'}), 400
    
    data = request.json
    
    # Create new application
    application = Application(
        job_id=job_id,
        applicant_id=user.id,
        cover_letter=data.get('cover_letter'),
        resume_filename=data.get('resume_filename')
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({'message': 'Application submitted successfully', 'application': application.to_dict()}), 201

@jobs_bp.route('/my-applications', methods=['GET'])
@login_required
def get_my_applications():
    """Get applications submitted by current job seeker"""
    user = User.query.get(session['user_id'])
    
    if user.user_type != 'job_seeker':
        return jsonify({'error': 'Only job seekers can view their applications'}), 403
    
    applications = Application.query.filter_by(applicant_id=user.id).order_by(Application.applied_at.desc()).all()
    
    return jsonify([app.to_dict() for app in applications])

@jobs_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@login_required
def update_application_status(application_id):
    """Update application status (job owner only)"""
    application = Application.query.get_or_404(application_id)
    user = User.query.get(session['user_id'])
    
    # Check if user owns the job this application is for
    if application.job.employer_id != user.id and user.user_type != 'admin':
        return jsonify({'error': 'You can only update applications for your own jobs'}), 403
    
    data = request.json
    status = data.get('status')
    
    if status not in ['pending', 'reviewed', 'accepted', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    application.status = status
    db.session.commit()
    
    return jsonify({'message': 'Application status updated successfully', 'application': application.to_dict()})

