# Django Admin Dashboard Backend

This project is a clean Django backend starter focused only on admin authentication and a custom admin dashboard. It is intentionally scoped so client login, team login, public registration, AI features, project management, ticketing, and requirement modules can be added later without rewriting the foundation.

## Tech Stack

- Django
- PostgreSQL or local SQLite
- Django Templates
- Bootstrap 5
- `django-environ`
- WhiteNoise for static file serving

## Features Included

- Admin-only login at `/dashboard/login/`
- Admin logout at `/dashboard/logout/`
- Protected dashboard pages for staff and superusers only
- Custom dashboard overview
- Admin profile update page
- Change password page
- Admin management list, create, detail, edit, activate, deactivate, and reset-password flows
- Password validation and CSRF protection
- Environment-based configuration via `.env`

## Project Structure

```text
core/
dashboard/
static/
static/dashboard/
templates/
templates/dashboard/
manage.py
requirements.txt
.env.example
```

## Setup

1. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create your environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Update `.env` with your real values:

   - `SECRET_KEY`
   - `DEBUG`
   - `ALLOWED_HOSTS`
   - `DATABASE_URL`

   Example local SQLite URL:

   ```env
   DATABASE_URL=sqlite:///db.sqlite3
   ```

   Example PostgreSQL URL:

   ```env
   DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/admin_dashboard
   ```

5. Run migrations:

   ```powershell
   python manage.py migrate
   ```

   If PostgreSQL authentication fails, double-check the username, password, host, port, and database name inside `DATABASE_URL`.

6. Create the first superuser/staff admin from env:

   Add these values to `.env`:

   ```env
   ADMIN_USERNAME=admin
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=change-this-password
   ```

   Then run:

   ```powershell
   python manage.py seed_admin
   ```

7. Start the development server:

   ```powershell
   python manage.py runserver
   ```

8. Open the dashboard login:

   ```text
   http://127.0.0.1:8000/dashboard/login/
   ```

## Admin Access Rules

- Only `is_staff=True` users can access dashboard pages.
- Inactive users cannot log in.
- Non-staff users cannot log in to the dashboard.
- Only logged-in admins can create new admins.
- New admins are always saved with `is_staff=True`.
- Only superusers can create or promote another superuser.
- `seed_admin` safely skips if the admin username or email already exists.
- `seed_admin` prints a clear error if `DATABASE_URL` is wrong or PostgreSQL rejects the credentials.

## Notes

- The default Django admin is available at `/django-admin/` for emergency maintenance, but the main workflow is the custom dashboard.
- Database configuration is environment-driven and supports PostgreSQL through `DATABASE_URL`.
- The built-in Django `User` model is used intentionally for now to keep the foundation simple and scalable.
