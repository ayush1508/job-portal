#!/usr/bin/env python3
"""
Database initialization script for Job Portal System
Creates default admin user and sample data
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.models.user import db, User, Job, Application

def init_database():
    """Initialize database with default admin user"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create default admin user
            admin = User(
                username='admin',
                email='admin@jobportal.com',
                user_type='admin',
                full_name='System Administrator'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create sample employer
            employer = User(
                username='techcorp',
                email='hr@techcorp.com',
                user_type='employer',
                full_name='Tech Corp HR',
                company_name='Tech Corp Solutions',
                phone='123-456-7890'
            )
            employer.set_password('employer123')
            db.session.add(employer)
            
            # Create sample job seeker
            job_seeker = User(
                username='johndoe',
                email='john.doe@email.com',
                user_type='job_seeker',
                full_name='John Doe',
                phone='098-765-4321'
            )
            job_seeker.set_password('seeker123')
            db.session.add(job_seeker)
            
            db.session.commit()
            
            # Create sample job
            sample_job = Job(
                title='Software Developer',
                description='We are looking for a skilled software developer to join our team.',
                location='New York, NY',
                salary='$70,000 - $90,000',
                requirements='Bachelor\'s degree in Computer Science, 2+ years experience with Python/Flask',
                employer_id=employer.id
            )
            db.session.add(sample_job)
            db.session.commit()
            
            print("Database initialized successfully!")
            print("Default users created:")
            print("Admin: username='admin', password='admin123'")
            print("Employer: username='techcorp', password='employer123'")
            print("Job Seeker: username='johndoe', password='seeker123'")
        else:
            print("Database already initialized!")

if __name__ == '__main__':
    init_database()

