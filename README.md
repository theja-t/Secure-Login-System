# Aegis Secure Login

A Django authentication starter with account creation, sign-in, a protected account page, CSRF-protected sign-out, password validation, and login lockouts.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ to sign in, or use **Create an account** to register. Failed logins are locked for one hour after five attempts.

## Production notes

Set `DJANGO_DEBUG=0`, a unique high-entropy `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS` before deployment. HTTPS is required in this mode; secure session and CSRF cookies, SSL redirection, and HSTS are enabled automatically. Use a production-grade database and configure email delivery before exposing the service publicly. Review `python manage.py check --deploy` for the final deployment environment.