# Deployment Guide

This guide provides step-by-step instructions for deploying the Job Portal System on Render and PythonAnywhere platforms.

## Prerequisites

Before deploying, ensure you have:
- A GitHub account with your project repository
- The project tested and working locally
- All dependencies listed in `requirements.txt`

## Deployment on Render

Render is a modern cloud platform that makes it easy to deploy web applications.

### Step 1: Prepare Your Repository

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Verify Files**
   Ensure these files are in your repository:
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - All source code in `src/` directory

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up for a free account
3. Connect your GitHub account

### Step 3: Deploy Web Service

1. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `job-portal-system` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Instance Type**: Free tier is sufficient for testing

3. **Environment Variables** (Optional)
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a secure secret key

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the build and deployment process

### Step 4: Initialize Database

1. **Access Web Service Shell**
   - Go to your service dashboard
   - Click "Shell" tab
   - Run: `python src/init_db.py`

2. **Verify Deployment**
   - Visit your Render URL
   - Test login with default accounts
   - Verify all functionality works

### Render Deployment Notes

- **Free Tier Limitations**: 
  - Service sleeps after 15 minutes of inactivity
  - 750 hours per month limit
  - Slower cold starts

- **Custom Domain**: Available on paid plans
- **SSL**: Automatically provided
- **Logs**: Available in the dashboard

## Deployment on PythonAnywhere

PythonAnywhere is a Python-focused hosting platform with excellent Flask support.

### Step 1: Create PythonAnywhere Account

1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Sign up for an account (free tier available)
3. Choose appropriate plan based on your needs

### Step 2: Upload Your Code

**Option A: Upload Files**
1. Go to "Files" tab in dashboard
2. Create a new directory: `/home/yourusername/job-portal-system`
3. Upload all project files

**Option B: Clone from GitHub**
1. Open a Bash console
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/job-portal-system.git
   cd job-portal-system
   ```

### Step 3: Set Up Virtual Environment

1. **Open Bash Console**
   ```bash
   cd job-portal-system
   python3.8 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python src/init_db.py
   ```

### Step 4: Configure Web App

1. **Create Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask" framework
   - Select Python 3.8

2. **Configure Paths**
   - **Source code**: `/home/yourusername/job-portal-system`
   - **Working directory**: `/home/yourusername/job-portal-system`

3. **Edit WSGI File**
   Replace the contents of the WSGI file with:
   ```python
   import sys
   import os
   
   # Add your project directory to sys.path
   project_home = '/home/yourusername/job-portal-system'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path
   
   # Set up the virtual environment
   activate_this = '/home/yourusername/job-portal-system/venv/bin/activate_this.py'
   with open(activate_this) as file_:
       exec(file_.read(), dict(__file__=activate_this))
   
   # Import your Flask application
   from src.main import app as application
   
   if __name__ == "__main__":
       application.run()
   ```

4. **Configure Static Files**
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/job-portal-system/src/static/`

### Step 5: Set Environment Variables

1. Go to "Files" tab
2. Edit `.bashrc` file
3. Add environment variables:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key-here
   ```

### Step 6: Reload and Test

1. **Reload Web App**
   - Go to "Web" tab
   - Click "Reload yourusername.pythonanywhere.com"

2. **Test Application**
   - Visit your PythonAnywhere URL
   - Test all functionality
   - Check error logs if issues occur

### PythonAnywhere Notes

- **Free Tier Limitations**:
  - One web app
  - Limited CPU seconds
  - No custom domains
  - HTTPS only on paid plans

- **Database**: SQLite works well for small applications
- **Logs**: Available in the "Web" tab
- **Console Access**: Always available for debugging

## Database Configuration for Production

### SQLite (Default)
- Works well for small to medium applications
- No additional setup required
- File-based storage

### MySQL (Recommended for Production)

1. **Update Database URI**
   In `src/main.py`, replace:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
   ```
   
   With:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@hostname/database_name'
   ```

2. **Install MySQL Dependencies**
   Add to `requirements.txt`:
   ```
   PyMySQL==1.0.2
   ```

3. **Update Models**
   Add to the top of `src/models/user.py`:
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

## Environment Variables

For production deployment, use environment variables for sensitive data:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Security Considerations

### Production Security Checklist

1. **Change Default Credentials**
   - Update admin password
   - Remove or change default test accounts

2. **Secure Secret Key**
   - Generate a strong, random secret key
   - Store in environment variables

3. **Database Security**
   - Use strong database passwords
   - Limit database access
   - Regular backups

4. **HTTPS**
   - Enable SSL/TLS certificates
   - Redirect HTTP to HTTPS

5. **Input Validation**
   - Validate all user inputs
   - Sanitize data before database storage

## Monitoring and Maintenance

### Health Checks
- Monitor application uptime
- Check database connectivity
- Verify user registration/login

### Backup Strategy
- Regular database backups
- Code repository backups
- Configuration backups

### Updates
- Keep dependencies updated
- Monitor security advisories
- Test updates in staging environment

## Troubleshooting

### Common Deployment Issues

1. **Build Failures**
   - Check `requirements.txt` for correct dependencies
   - Verify Python version compatibility
   - Check for syntax errors

2. **Database Issues**
   - Ensure database initialization script runs
   - Check file permissions
   - Verify database connection string

3. **Static Files Not Loading**
   - Configure static file serving
   - Check file paths
   - Verify permissions

4. **Import Errors**
   - Check Python path configuration
   - Verify virtual environment setup
   - Check module imports

### Getting Help

1. **Platform Documentation**
   - Render: [render.com/docs](https://render.com/docs)
   - PythonAnywhere: [help.pythonanywhere.com](https://help.pythonanywhere.com)

2. **Logs and Debugging**
   - Check application logs
   - Use platform debugging tools
   - Test locally first

3. **Community Support**
   - Platform-specific forums
   - Stack Overflow
   - GitHub issues

## Cost Considerations

### Free Tier Limitations

**Render Free Tier:**
- 750 hours per month
- Service sleeps after inactivity
- Limited bandwidth

**PythonAnywhere Free Tier:**
- One web app
- Limited CPU seconds
- No custom domains

### Upgrade Benefits

**Paid Plans Include:**
- Custom domains
- SSL certificates
- Better performance
- More resources
- Priority support

## Conclusion

Both Render and PythonAnywhere offer excellent platforms for deploying Flask applications. Choose based on your specific needs:

- **Render**: Better for modern deployment workflows, automatic deployments from Git
- **PythonAnywhere**: Better for Python-specific hosting, more traditional hosting approach

Follow this guide step-by-step, and your Job Portal System will be successfully deployed and accessible to users worldwide.

