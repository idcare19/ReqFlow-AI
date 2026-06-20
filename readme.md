# ReqFlow AI

### AI-Powered Requirement Analysis and Task Planning Platform

ReqFlow AI is a smart planning platform for agencies, project managers, and development teams. It is designed to convert raw client requirements into structured, development-ready plans.

The long-term vision is to use AI to analyze requirements and suggest features, modules, tasks, APIs, database structures, timelines, and execution plans, while keeping final control with the project manager or admin.

**Transform Requirements Into Action.**

---

## Vision

ReqFlow AI is built to reduce project planning time and improve delivery clarity.

Instead of manually converting client requirements into tasks, the platform aims to generate structured suggestions in minutes.

**AI-assisted planning. Human-controlled execution.**

---

## Problem

In software agencies and development teams, planning usually takes significant manual effort.

Common problems:

- Client requirements are often unstructured
- Project managers spend hours breaking requirements into tasks
- API and database planning takes extra time
- Sprint planning is handled manually
- Teams may misunderstand scope
- Clients do not always get clear project visibility

---

## Solution

ReqFlow AI solves this by acting as a planning assistant.

Clients or admins will be able to submit project requirements, and the platform will analyze them to generate planning suggestions. Project managers or admins can then review, edit, approve, or reject the suggested output before creating the final project.

---

## Platform Flow

```text
Client Requirement
        ↓
AI Requirement Analysis
        ↓
AI Suggested Output
        ↓
Project Manager Review
        ↓
Project Creation
        ↓
Task Editing and Assignment
        ↓
Development Tracking
        ↓
Project Delivery
        ↓
Ticket Support System
```

---

## AI Suggested Output

ReqFlow AI is planned to suggest:

- Project features
- Development modules
- Task breakdown
- API endpoints
- Database tables
- Sprint plan
- Timeline estimate
- Technical architecture
- Testing checklist

---

## Human Control

AI will not directly create the final project.

The project manager or admin will:

- Review AI output
- Edit suggested tasks
- Add custom tasks
- Remove unnecessary tasks
- Create the final project manually
- Assign tasks to team members
- Track progress

This keeps the platform practical and safe for real agency workflows.

---

## Current Features

### Admin Dashboard

- Admin-only login
- Admin logout
- Secure dashboard access
- Admin profile management
- Change password
- Admin management
- Protected dashboard routes
- Staff-only and superuser-only access control

### Security

- CSRF protection
- Secure session settings
- Password validation
- Inactive-user login prevention
- Environment-based configuration

### Developer Setup

- SQLite local database support
- PostgreSQL-ready `DATABASE_URL` support
- Env-based first admin seeding with `python manage.py seed_admin`
- Session-based JSON auth APIs for frontend integration

---

## Current Status

### Phase 1 Completed

- Admin authentication
- Custom admin dashboard
- Admin management
- Bootstrap template UI
- Protected dashboard routes
- Environment-based settings
- Local SQLite setup
- PostgreSQL-ready configuration
- Seed command for first admin

### Upcoming Modules

- Requirement submission
- AI analysis engine
- Task suggestion system
- Project management
- Team management
- Client portal
- Ticket support system
- Reports and analytics

---

## Tech Stack

### Backend

- Django
- PostgreSQL
- SQLite for local development
- Django Templates

### Frontend

- Bootstrap 5
- HTML
- CSS
- JavaScript

### Planned AI Layer

- Google Gemini API
- OpenAI API support

---

## Security Features

- Admin-only authentication
- Staff-only dashboard access
- CSRF protection
- Secure sessions
- Password validation
- Environment variable configuration
- Protected dashboard views

---

## Planned Modules

```text
ReqFlow AI
│
├── Admin Dashboard
├── Requirement Management
├── AI Analysis Engine
├── Task Suggestion System
├── Project Management
├── Team Management
├── Client Portal
├── Ticket Management
└── Reports and Analytics
```

---

## Project Structure

```text
core/
dashboard/
dashboard/management/commands/
static/
static/dashboard/
templates/
templates/dashboard/
manage.py
requirements.txt
.env.example
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/idcare19/ReqFlow-AI.git
cd ReqFlow-AI
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

Create a `.env` file from `.env.example`.

```bash
copy .env.example .env
```

Use local SQLite by default:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-this-password
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://reqflow-ai.onrender.com
SESSION_COOKIE_SAMESITE=Lax
CSRF_COOKIE_SAMESITE=Lax
```

If you want PostgreSQL instead, replace `DATABASE_URL` with your PostgreSQL connection string.

For Render, also set:

```env
ALLOWED_HOSTS=127.0.0.1,localhost,reqflow-ai.onrender.com
RENDER_EXTERNAL_HOSTNAME=reqflow-ai.onrender.com
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create First Staff Admin

```bash
python manage.py seed_admin
```

The command safely skips if the admin already exists.

### 8. Run Server

```bash
python manage.py runserver
```

### 9. Open Dashboard

```text
http://127.0.0.1:8000/dashboard/login/
```

### 10. Health Check

Use this lightweight route for uptime checks or Render keep-alive pings:

```text
/health/
```

Example local URL:

```text
http://127.0.0.1:8000/health/
```

### 11. Frontend Auth APIs

These JSON endpoints use Django session authentication and keep the dashboard HTML login flow unchanged.

```text
POST /api/auth/login/
POST /api/auth/logout/
GET /api/auth/me/
GET /api/health/
```

Example login payload:

```json
{
  "username": "admin",
  "password": "password"
}
```

Notes:

- Only `is_staff=True` users can log in through the API
- Inactive users are blocked
- Use Django CSRF tokens for frontend `POST` requests
- `GET /api/auth/me/` also sets the CSRF cookie for frontend usage
- For cross-domain frontend apps, configure `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`
- For HTTPS cross-site cookies in production, set `SESSION_COOKIE_SAMESITE=None` and `CSRF_COOKIE_SAMESITE=None`

---

## Repository Description

```text
AI-powered requirement analysis platform that helps convert client requirements into structured plans, tasks, modules, and future project workflows.
```

---

## Suggested GitHub Topics

```text
django
python
postgresql
sqlite
bootstrap5
ai
requirement-analysis
task-generation
project-management
admin-dashboard
workflow-automation
agency-tools
```

---

## Target Users

- Software agencies
- Freelancers
- Project managers
- Product managers
- Startup teams
- Development teams

---

## Repository

GitHub: `idcare19/ReqFlow-AI`

URL: `https://github.com/idcare19/ReqFlow-AI`

---

## License

This project is currently under active development.

© ReqFlow AI
