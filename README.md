# CampusConnect

**Full name:** Darryll Eral

**Section:** CSIT327-G1

CampusConnect is a Django application with sign-up and login, a dashboard, and a protected profile page where each logged-in user can update their own details.

## Run locally

1. Install Python 3.11 or later.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. (Optional) Set a local Django secret key in PowerShell. If omitted, Django uses a development-only fallback from settings.

   ```powershell
   $env:DJANGO_SECRET_KEY = "replace-with-a-random-local-secret"
   ```

5. Create the local database and start the development server:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

6. Visit http://127.0.0.1:8000/ and create an account.

The SQLite database is created locally and is intentionally excluded from Git. For deployment, set a unique, strong `DJANGO_SECRET_KEY`; do not use the development fallback.
