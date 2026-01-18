# Online Lucky Draw System

A web application for running fair, auditable, and user‑friendly lucky draws. This README explains what the project does, how it works, how to set it up locally, the database configuration (name and connection examples), user roles and responsibilities, and common operational tasks and troubleshooting steps.

---

## Overview

**Purpose**  
The Online Lucky Draw System enables event organizers, businesses, and individuals to run randomized prize draws online. It replaces manual ticketing and paper processes with a transparent, reproducible, and auditable digital workflow.

**Key goals**
- Provide a secure, fair random selection algorithm.
- Let participants register, join draws, and view results in real time.
- Give organizers tools to create draws, manage entries, and publish winners.
- Offer administrators dashboards and reports to monitor activity and health.

---

Paste this into your `settings.py`. It reads the `.env` variables using `os.environ`. No extra packages required.

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Basic env helpers
def env(key, default=None):
    return os.environ.get(key, default)

SECRET_KEY = env('DJANGO_SECRET_KEY', 'unsafe-default-for-dev-only')
DEBUG = env('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = [h.strip() for h in env('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

# Database selection
DB_ENGINE = env('DB_ENGINE', 'sqlite').lower()

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME', 'lucky_draw_db'),
            'USER': env('DB_USER', 'db_user'),
            'PASSWORD': env('DB_PASSWORD', 'db_password'),
            'HOST': env('DB_HOST', '127.0.0.1'),
            'PORT': env('DB_PORT', '3306'),
            'OPTIONS': {
                # ensure strict mode for data integrity
                'init_command': env('DB_OPTIONS_INIT_COMMAND', "SET sql_mode='STRICT_TRANS_TABLES'"),
                # adjust charset if needed
                'charset': 'utf8mb4',
            },
        }
    }

else:  # sqlite fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(Path(env('SQLITE_PATH', BASE_DIR / 'db.sqlite3'))),
        }
    }
```


## Features

**Participant features**
- Account registration and login.
- Browse active and upcoming draws.
- Enter draws (free or paid depending on event rules).
- View personal entries and past wins.

**Organizer features**
- Create and configure draws (title, prize, winners count, schedule, rules).
- Approve or verify entries.
- Run winner selection (manual quick select or advanced selection with seed/force).
- Export or view winners and audit logs.

**Admin features**
- Global dashboard with statistics (total draws, entries, winners).
- Per‑draw analytics and participant management.
- System maintenance tools (migrations, backups, user management).

**System features**
- Support for single‑winner and multi‑winner draws.
- Randomized selection algorithm with optional seed for reproducibility.
- Notifications (email/SMS hooks) to inform winners.
- Audit trail: store which entry won, timestamp, method, and seed.

---

## Architecture and Data Model

**High level components**
- **Web frontend**: Django templates + Bootstrap for admin and user interfaces.
- **Backend**: Django app (`accounts`) with views for dashboard, draw pages, selection endpoints.
- **Database**: Relational DB (MySQL/MariaDB recommended for production; SQLite for quick local testing).
- **Optional services**: SMTP for email, SMS provider for texts, reverse proxy (Nginx) for production.

**Core models**
- **User / Profile**: authentication and role (admin, organizer, user).
- **Draw**: metadata (title, prize, start/end/result dates, winners_count, draw_type).
- **Entry**: a user’s participation record for a draw (is_active, is_verified).
- **Winner**: stores draw, entry (nullable), user, position, selected_at, method, seed, audit_note.
- **EntryAdminAction**: audit actions performed by admins on entries.

**Selection algorithm (summary)**
- Collect eligible entries: `Entry.objects.filter(draw_id=..., is_active=True, is_verified=True)`.
- Build a user→entries map to avoid duplicate winners per user unless draw type allows multiple wins.
- Use a secure RNG (optionally seeded) to pick winners and persist them to `Winner` with `selected_at` and `entry_id`.

---

## Setup and Configuration

**Repository**
- Clone the project repository to your machine.

**Environment**
- Python 3.10+ recommended.
- Virtual environment (venv) recommended.

**Environment variables**
Create a `.env` or set environment variables for sensitive settings:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DATABASE_URL=mysql://db_user:db_password@127.0.0.1:3306/lucky_draw_db
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

**Database name and connection examples**

- **Recommended production database name**
  - **Database name**: `lucky_draw_db`

- **MySQL / MariaDB connection example**
  - **Connection string**:
    ```
    mysql://db_user:db_password@127.0.0.1:3306/lucky_draw_db
    ```
  - **Django DATABASES example**:
    ```python
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lucky_draw_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
    }
    ```

- **SQLite (local development)**
  - **File**: `db.sqlite3`
  - **Django DATABASES example**:
    ```python
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
      }
    }
    ```

**Install and run locally**

```bash
# create venv and activate
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# create database (MySQL): create database lucky_draw_db and grant user privileges
# then run migrations
python manage.py makemigrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

# run dev server
python manage.py runserver
```

**Migrations and schema notes**
- Always run `makemigrations` and `migrate` after model changes.
- If a migration fails because a column is missing or a DROP fails, inspect the failing migration and either:
  - fix the migration to use conditional SQL, or
  - use `python manage.py migrate <app> <migration_name> --fake` carefully after confirming schema state.
- Back up the database before editing migration history.

---

## Roles and Permissions

**Admin**
- Full system access.
- Manage users, draws, entries, and system settings.
- Run and force winner selection.
- View analytics and audit logs.

**Organizer**
- Create and configure draws.
- Manage entries for their draws (verify, deactivate).
- Trigger winner selection for their draws (if allowed).
- View draw‑level analytics.

**User (Participant)**
- Register and maintain profile.
- Browse draws and enter eligible draws.
- View personal entries and past wins.
- Receive notifications if selected.

**Role enforcement**
- Views and endpoints are protected by decorators or permission checks (e.g., `@login_required` and role checks via `Profile.role`).
- Admin-only pages should check `request.user.profile.role == 'admin'`.
- Organizer actions should be limited to draws they created or are assigned to manage.

---

## Operations and Troubleshooting

**Common tasks**
- **Run selection**: Admin/organizer triggers selection via dashboard or API. Winners are saved to `Winner` with `selected_at` and `entry_id`.
- **Force replace winners**: Use the “Force” option to delete existing winners and re-run selection.
- **Notifications**: Configure SMTP and SMS provider credentials in environment variables.

**Common errors and fixes**
- **Unknown column accounts_winner.entry_id**
  - Cause: model expects `entry` FK but DB column missing.
  - Fix: ensure `accounts/models.py` defines `entry = models.ForeignKey(Entry, ...)`, then run:
    ```bash
    python manage.py makemigrations accounts
    python manage.py migrate
    ```
    If migration fails because a previous migration tries to drop a column that does not exist, either edit that migration to use conditional SQL or mark it applied with:
    ```bash
    python manage.py migrate accounts <migration_number> --fake
    ```
    Always back up DB before faking migrations.

- **TemplateSyntaxError for unclosed tags**
  - Cause: mismatched `{% for %}` / `{% endfor %}` or invalid expressions (parentheses inside `{% if %}`).
  - Fix: remove stray blocks or rewrite conditionals without parentheses (use `and`/`or`).

**Testing**
- Unit tests for selection algorithm and model behavior.
- Manual test flow:
  1. Create draw and add entries (set `is_active=True`, `is_verified=True`).
  2. As admin, run selection (AJAX or POST).
  3. Confirm `Winner` rows created with `entry_id`, `user_id`, `position`, and `selected_at`.
  4. Verify notifications are sent if configured.

**Backups and maintenance**
- Regular DB backups (mysqldump or managed DB snapshots).
- Monitor logs for OperationalError and migration issues.
- Keep dependencies up to date and test migrations in a staging environment before production.

---

## API Endpoints and URLs (examples)

- `GET /accounts/dashboard/admin/` — Admin dashboard.
- `GET /accounts/draws/<id>/` — Draw detail page for participants.
- `GET /accounts/draws/<id>/winner-selection/` — Winner selection page (view and run).
- `POST /accounts/draws/<id>/select-winners/` — Endpoint to run selection (supports AJAX).
- `GET /accounts/draws/<id>/participants/` — View participants for a draw.

---

## Security and Compliance

- Use HTTPS in production.
- Store secrets in environment variables, not in source control.
- Use database permissions and least privilege for DB users.
- Sanitize and validate all user input.

### .env.example

Copy this file to `.env` and fill in the values before running the project.

```env
# Django core
DJANGO_SECRET_KEY=replace-with-a-secure-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Choose database type: mysql or sqlite
DB_ENGINE=mysql

# MySQL / MariaDB settings
DB_NAME=lucky_draw_db
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_OPTIONS_INIT_COMMAND=SET sql_mode='STRICT_TRANS_TABLES'

# SQLite settings (used when DB_ENGINE=sqlite)
SQLITE_PATH=db.sqlite3

# Email (example)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

---

### Django settings snippet with exact DATABASES blocks

Paste this into your `settings.py`. It reads the `.env` variables using `os.environ`. No extra packages required.

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Basic env helpers
def env(key, default=None):
    return os.environ.get(key, default)

SECRET_KEY = env('DJANGO_SECRET_KEY', 'unsafe-default-for-dev-only')
DEBUG = env('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = [h.strip() for h in env('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

# Database selection
DB_ENGINE = env('DB_ENGINE', 'sqlite').lower()

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME', 'lucky_draw_db'),
            'USER': env('DB_USER', 'db_user'),
            'PASSWORD': env('DB_PASSWORD', 'db_password'),
            'HOST': env('DB_HOST', '127.0.0.1'),
            'PORT': env('DB_PORT', '3306'),
            'OPTIONS': {
                # ensure strict mode for data integrity
                'init_command': env('DB_OPTIONS_INIT_COMMAND', "SET sql_mode='STRICT_TRANS_TABLES'"),
                # adjust charset if needed
                'charset': 'utf8mb4',
            },
        }
    }

else:  # sqlite fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(Path(env('SQLITE_PATH', BASE_DIR / 'db.sqlite3'))),
        }
    }
```

---

### Quick usage notes

- **Switch database**: set `DB_ENGINE=mysql` for MySQL or `DB_ENGINE=sqlite` for local development.  
- **MySQL prerequisites**: create the database and grant the user privileges before running migrations:
  ```bash
  # example (MySQL shell)
  CREATE DATABASE lucky_draw_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
  CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'db_password';
  GRANT ALL PRIVILEGES ON lucky_draw_db.* TO 'db_user'@'localhost';
  FLUSH PRIVILEGES;
  ```
- **Run migrations**:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- **Security**: never commit `.env` to source control. Use a secure `DJANGO_SECRET_KEY` in production and set `DEBUG=False`.

---

### Troubleshooting tips

- If you see `Unknown column accounts_winner.entry_id`, ensure:
  - `accounts/models.py` defines the `entry` ForeignKey on `Winner`.
  - You ran `makemigrations` and `migrate` after model changes.
- If migrations fail due to a missing column in an existing migration, inspect the failing migration and either:
  - fix the migration to use conditional SQL, or
  - mark the migration as applied with `python manage.py migrate accounts <migration_name> --fake` after confirming the schema state.
