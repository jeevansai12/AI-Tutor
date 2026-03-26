# Setup and Deployment Guide

## Local Development Setup

### Prerequisites

- Python 3.9+ installed
- pip (Python package manager)
- Git (optional, but recommended)

### Step 1: Clone and Navigate

```bash
cd ai_tutor
```

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies.

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- Django (web framework)
- python-dotenv (load .env file)
- google-generativeai (AI API client)

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
```

**Note:** The `.env` file is already in `.gitignore` (not pushed to Git).

### Step 5: Run Migrations

Initialize the database:

```bash
python manage.py migrate
```

This creates `db.sqlite3` with all required tables.

### Step 6: Load Sample Questions

```bash
python manage.py load_questions
```

This populates the database with sample MCQ questions.

### Step 7: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:

```
Username: admin
Email: admin@example.com
Password: (enter password)
Password (again): (confirm)
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Output:

```
Starting development server at http://127.0.0.1:8000/
```

Open browser → `http://127.0.0.1:8000/`

### Step 9: Access Admin Panel

Go to: `http://127.0.0.1:8000/admin/`

Login with superuser credentials.

Here you can:

- Add/edit questions
- View quiz results
- Read feedback
- Add/edit flashcards

---

## User Workflow

### 1. Register New Account

- Go to `/register/`
- Create username and password
- Account created and auto-logged in

### 2. Quiz (Primary Feature)

- Click "Take Quiz"
- Select subject (Python, DBMS, etc.)
- Answer MCQs
- See results with:
  - Score percentage
  - Performance level (Beginner/Intermediate/Advanced)
  - Personalized recommendation

### 3. Chat with AI

- Click "Chat"
- Enter your Google Gemini API key (get from: https://makersuite.google.com/app/apikey)
- Ask questions
- AI explains concepts

### 4. Generate Notes

- Click "Notes"
- Enter a topic (e.g., "Python loops")
- AI generates study notes

### 5. Flashcards

- Click "Flashcards"
- Select subject
- Review and click to reveal answers

### 6. Feedback

- Click "Feedback"
- Submit suggestions or bug reports

---

## Production Deployment

### Database

**Development (local):** SQLite (`db.sqlite3`)

**Production:** PostgreSQL recommended

#### Change to PostgreSQL:

1. Install PostgreSQL
2. Create database:

```sql
CREATE DATABASE aitutor_db;
CREATE USER aitutor_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE aitutor_db TO aitutor_user;
```

3. Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aitutor_db',
        'USER': 'aitutor_user',
        'PASSWORD': 'strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

### Django Settings for Production

Update `aitutor/settings.py`:

```python
# Security
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.getenv('SECRET_KEY')  # Load from env

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-password'
```

### Hosting Options

#### Option 1: PythonAnywhere (Easiest for Beginners)

1. Sign up at https://www.pythonanywhere.com/
2. Upload your code
3. Configure web app (Django, Python 3.x)
4. Set environment variables
5. Reload web app
6. Live at `yourusername.pythonanywhere.com`

#### Option 2: Heroku

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create aitutor-app
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Option 3: DigitalOcean / AWS / Google Cloud

1. Create a Linux VM
2. SSH into server
3. Install Python, PostgreSQL, nginx
4. Clone project
5. Set up gunicorn (WSGI server)
6. Configure nginx (reverse proxy)
7. Set up SSL with Let's Encrypt

### Collect Static Files

Before deploying:

```bash
python manage.py collectstatic --noinput
```

This gathers all CSS, JS, images in `staticfiles/` folder.

### Environment Variables for Production

Create `.env` file on server:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
GEMINI_API_KEY=user-provides-their-own
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/aitutor_db
```

### Backup Database

```bash
# Export
python manage.py dumpdata > backup.json

# Import
python manage.py loaddata backup.json
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'django'"

**Solution:** Activate virtual environment and run:

```bash
pip install -r requirements.txt
```

### Problem: "Port 8000 is already in use"

**Solution:** Use different port:

```bash
python manage.py runserver 8001
```

### Problem: "No such table: core_question"

**Solution:** Run migrations:

```bash
python manage.py migrate
```

### Problem: "Gemini API returns error"

**Solution:**

- Check API key is valid (from makersuite.google.com)
- Check internet connection
- Check API quota isn't exceeded

### Problem: "Static files not loading in production"

**Solution:**

```bash
python manage.py collectstatic --noinput
# Configure web server (nginx/Apache) to serve /static/ folder
```

---

## Commands Reference

| Command                            | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| `python manage.py runserver`       | Start dev server                              |
| `python manage.py migrate`         | Apply database changes                        |
| `python manage.py makemigrations`  | Create migration files (after editing models) |
| `python manage.py createsuperuser` | Create admin account                          |
| `python manage.py shell`           | Interactive Python shell with Django context  |
| `python manage.py load_questions`  | Load sample questions                         |
| `python manage.py test`            | Run test suite                                |
| `python manage.py collectstatic`   | Gather static files for production            |

---

## Performance Tips

### For Local Development

- SQLite is fine
- Debug toolbar helps: `pip install django-debug-toolbar`
- Logging helps identify bottlenecks

### For Production

1. **Database Indexing**

   ```python
   # In models
   class Question(models.Model):
       subject = CharField(db_index=True)  # Add index
   ```

2. **Caching**

   ```python
   from django.views.decorators.cache import cache_page

   @cache_page(60)  # Cache for 60 seconds
   def quiz_select_view(request):
       ...
   ```

3. **Async Views** (if needed)

   ```python
   from asgiref.sync import sync_to_async

   async def my_async_view(request):
       data = await sync_to_async(get_data)()
       return JsonResponse(data)
   ```

But for a BCA project, these optimizations are **NOT needed**. Keep it simple!

---

## Security Checklist

- [x] Use strong SECRET_KEY (> 50 characters)
- [x] Set DEBUG = False in production
- [x] Use HTTPS (SSL certificate)
- [x] Hash passwords (Django does this automatically)
- [x] Validate all user inputs (Django forms do this)
- [x] Use CSRF tokens (Django templates include {% csrf_token %})
- [x] Set ALLOWED_HOSTS correctly
- [x] Never commit `.env` file to Git
- [x] Use environment variables for secrets
- [x] Regularly update Django and dependencies

---

## Maintenance

### Update Dependencies

```bash
pip list --outdated
pip install --upgrade package-name
```

### Database Backup

```bash
# Local SQLite
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL
pg_dump aitutor_db > backup.sql
```

### Monitor Logs

```bash
# Django logs
tail -f /var/log/django.log

# Web server logs
tail -f /var/log/nginx/error.log
```

---

## Next Steps After Deployment

1. **Set up monitoring:** Use tools like Sentry for error tracking
2. **Add analytics:** Track user behavior (Google Analytics)
3. **Set up email:** Send notifications to admins
4. **Backups:** Automated daily backups
5. **Tests:** Write unit tests for each feature
6. **CI/CD:** Use GitHub Actions for automated testing and deployment

---

## Questions?

- **Django Docs:** https://docs.djangoproject.com/
- **Deployment Guide:** https://docs.djangoproject.com/en/stable/howto/deployment/
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/django
