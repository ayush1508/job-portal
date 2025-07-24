# Job Portal System

A minimal web-based Job Portal System built with Flask backend, SQLite database, and simple HTML/CSS frontend. This system provides comprehensive functionality for employers, job seekers, and administrators to manage job postings and applications.

## Features

### Core Functionality
- **User Authentication**: Secure registration and login system with session management
- **Role-based Access Control**: Three distinct user types (Employer, Job Seeker, Admin)
- **Job Management**: Complete CRUD operations for job postings
- **Application System**: Job seekers can apply to jobs with cover letters
- **Search & Filter**: Advanced search functionality by title, location, and keywords
- **Admin Dashboard**: Comprehensive management interface with statistics

### User Modules

#### 1. Employer Module
- Register/Login as employer
- Post new job listings with detailed information
- View and manage their job postings
- View applications received for their jobs
- Delete job postings

#### 2. Job Seeker Module
- Register/Login as job seeker
- Browse all available jobs
- Search and filter jobs by various criteria
- Apply to jobs with cover letters
- Track application status
- View application history

#### 3. Admin Module
- Login with admin privileges
- View comprehensive dashboard with statistics
- Manage all users (view and delete)
- Manage all job postings (view and delete)
- View all applications across the platform
- Monitor platform activity

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily configurable for MySQL)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: Flask sessions with password hashing
- **Styling**: Minimal responsive CSS design

## Project Structure

```
job-portal-system/
├── src/
│   ├── models/
│   │   └── user.py              # Database models (User, Job, Application)
│   ├── routes/
│   │   ├── user.py              # Authentication and user management routes
│   │   ├── jobs.py              # Job management and application routes
│   │   └── admin.py             # Admin dashboard and management routes
│   ├── static/
│   │   ├── index.html           # Single-page application frontend
│   │   └── favicon.ico          # Website icon
│   ├── database/
│   │   └── app.db               # SQLite database file
│   ├── main.py                  # Flask application entry point
│   └── init_db.py               # Database initialization script
├── venv/                        # Virtual environment
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd job-portal-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python src/init_db.py
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

### Default User Accounts

The database initialization script creates three default accounts for testing:

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| admin | admin123 | Admin | System administrator with full access |
| techcorp | employer123 | Employer | Sample employer account (Tech Corp Solutions) |
| johndoe | seeker123 | Job Seeker | Sample job seeker account |

## Deployment

### Deployment on Render

1. **Prepare for deployment**
   - Ensure all dependencies are in `requirements.txt`
   - Verify the application runs locally

2. **Create Render account**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub account

3. **Deploy the application**
   - Create a new Web Service
   - Connect your GitHub repository
   - Configure build and start commands:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python src/main.py`
   - Set environment variables if needed

4. **Initialize database**
   - After deployment, run the database initialization script once

### Deployment on PythonAnywhere

1. **Create PythonAnywhere account**
   - Sign up at [pythonanywhere.com](https://pythonanywhere.com)
   - Choose an appropriate plan

2. **Upload your code**
   - Use the Files tab to upload your project
   - Or clone from GitHub using the console

3. **Set up virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.8 jobportal
   pip install -r requirements.txt
   ```

4. **Configure web app**
   - Go to Web tab and create a new web app
   - Choose Flask framework
   - Set the source code directory
   - Configure WSGI file to point to your Flask app

5. **Initialize database**
   ```bash
   python src/init_db.py
   ```

### Environment Configuration

For production deployment, consider these configurations:

1. **Security Settings**
   - Change the SECRET_KEY in `main.py`
   - Use environment variables for sensitive data
   - Enable HTTPS in production

2. **Database Configuration**
   - For MySQL, update the database URI in `main.py`
   - Set up proper database credentials
   - Configure database backups

3. **Performance Optimization**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Configure static file serving
   - Enable caching if needed

## API Endpoints

### Authentication Endpoints
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/profile` - Get current user profile
- `PUT /api/profile` - Update user profile

### Job Management Endpoints
- `GET /api/jobs` - Get all jobs (with search/filter)
- `GET /api/jobs/<id>` - Get specific job details
- `POST /api/jobs` - Create new job (employers only)
- `PUT /api/jobs/<id>` - Update job (job owner only)
- `DELETE /api/jobs/<id>` - Delete job (job owner/admin only)
- `GET /api/my-jobs` - Get employer's jobs

### Application Endpoints
- `POST /api/jobs/<id>/apply` - Apply to a job
- `GET /api/my-applications` - Get user's applications
- `GET /api/jobs/<id>/applications` - Get job applications (employer only)
- `PUT /api/applications/<id>/status` - Update application status

### Admin Endpoints
- `GET /api/admin/dashboard` - Get admin dashboard stats
- `GET /api/admin/users` - Get all users
- `DELETE /api/admin/users/<id>` - Delete user
- `GET /api/admin/jobs` - Get all jobs
- `DELETE /api/admin/jobs/<id>` - Delete job
- `GET /api/admin/applications` - Get all applications

## Database Schema

### User Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `user_type` (employer/job_seeker/admin)
- `full_name`
- `phone`
- `company_name` (for employers)
- `created_at`

### Job Table
- `id` (Primary Key)
- `title`
- `description`
- `location`
- `salary`
- `requirements`
- `employer_id` (Foreign Key to User)
- `created_at`
- `is_active`

### Application Table
- `id` (Primary Key)
- `job_id` (Foreign Key to Job)
- `applicant_id` (Foreign Key to User)
- `cover_letter`
- `resume_filename`
- `applied_at`
- `status` (pending/reviewed/accepted/rejected)

## Usage Guide

### For Employers

1. **Registration**
   - Click "Register" and select "Employer" as user type
   - Fill in company information
   - Complete registration

2. **Posting Jobs**
   - Login and access Employer Dashboard
   - Click "Post New Job"
   - Fill in job details (title, location, salary, description, requirements)
   - Submit the job posting

3. **Managing Applications**
   - View your posted jobs in "My Jobs"
   - Click "View Applications" to see applicants
   - Review cover letters and applicant information

### For Job Seekers

1. **Registration**
   - Click "Register" and select "Job Seeker" as user type
   - Fill in personal information
   - Complete registration

2. **Finding Jobs**
   - Browse available jobs on the main page
   - Use search filters to find relevant positions
   - Click "View Details" for more information

3. **Applying for Jobs**
   - Click "Apply" on desired job postings
   - Write a cover letter
   - Submit application

4. **Tracking Applications**
   - Access Job Seeker Dashboard
   - Click "My Applications" to view application status

### For Administrators

1. **Login**
   - Use admin credentials to access admin dashboard
   - View platform statistics

2. **User Management**
   - Click "Manage Users" to view all registered users
   - Delete users if necessary (except admin accounts)

3. **Job Management**
   - Click "Manage Jobs" to view all job postings
   - Delete inappropriate or expired job postings

4. **Application Monitoring**
   - Click "View Applications" to see all applications
   - Monitor platform activity

## Customization

### Styling
- Modify `src/static/index.html` for layout changes
- Update CSS styles in the `<style>` section
- Add Bootstrap or other CSS frameworks if desired

### Database
- Update connection string in `src/main.py` for different databases
- Modify models in `src/models/user.py` for additional fields
- Create migration scripts for schema changes

### Features
- Add file upload functionality for resumes
- Implement email notifications
- Add job categories and tags
- Include salary range filters
- Add company profiles

## Troubleshooting

### Common Issues

1. **Database Errors**
   - Delete `src/database/app.db` and run `python src/init_db.py`
   - Check file permissions for database directory

2. **Import Errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port in `src/main.py`: `app.run(host='0.0.0.0', port=5001)`
   - Kill existing processes using the port

4. **CORS Issues**
   - Ensure Flask-CORS is properly configured
   - Check browser console for specific CORS errors

### Development Tips

1. **Debug Mode**
   - Debug mode is enabled by default in `main.py`
   - Disable for production deployment

2. **Database Reset**
   - Run `python src/init_db.py` to reset database with sample data
   - Backup important data before resetting

3. **Testing**
   - Use the default accounts for testing different user roles
   - Test all CRUD operations before deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes. Feel free to use and modify as needed for your college projects.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Test with default user accounts
4. Verify all dependencies are installed

## Future Enhancements

- File upload for resumes and company logos
- Email notification system
- Advanced search with filters
- Job recommendation system
- Mobile application
- Integration with external job boards
- Analytics and reporting features
- Multi-language support

