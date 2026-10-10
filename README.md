# Feminine Aura Backend

A Django REST API backend for the Feminine Aura platform, built to power a modern feminine wellness brand experience with secure authentication, payments, media support, and deployment-ready configuration.

## Overview

This project provides the server-side foundation for the Feminine Aura ecosystem. It includes Django, Django REST Framework, JWT authentication, CORS configuration, Stripe payment support, and static/media handling for deployment on Render.

## Features

- Django 5 + DRF API layer
- JWT-based authentication with Simple JWT
- CORS support for frontend domains and Vercel deployments
- SQLite default database with support for external database URLs
- Stripe integration for payments
- Static file serving via WhiteNoise
- AWS S3-ready media storage configuration support
- Admin dashboard for managing site content and data
- Render deployment configuration included

## Tech Stack

- Python 3
- Django 5.2
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL-compatible database support via dj-database-url
- Stripe API
- django-storages + boto3 for cloud media storage
- WhiteNoise for static files
- Render deployment

## Project Structure

```bash
feminineaurabackend/
├── feminine_aura/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
├── static/
├── staticfiles/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── render.yaml
├── .env
└── README.md
```

## Prerequisites

- Python 3.10+
- pip
- virtualenv or venv
- Git

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/naseemsuleiman/feminineaurabackend.git
cd feminineaurabackend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables (recommended via `.env`):

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:////absolute/path/to/db.sqlite3
PAYSTACK_SECRET_KEY=your-paystack-secret
PAYSTACK_PUBLIC_KEY=your-paystack-public
```

5. Run database migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://localhost:8000
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key for app security |
| `DEBUG` | No | Enables debug mode in development |
| `DATABASE_URL` | No | Database connection string |
| `PAYSTACK_SECRET_KEY` | No | Secret key for Paystack payments |
| `PAYSTACK_PUBLIC_KEY` | No | Public key for Paystack frontend integration |

## API Configuration

This backend uses Django REST Framework with JWT authentication. The default authentication settings allow public access unless explicitly restricted by views.

### JWT settings

The project is configured with:

- Access token lifetime: 7 days
- Refresh token lifetime: 30 days

## CORS

The project allows cross-origin requests from:

- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `https://feminine-aura.com`
- `https://www.feminine-aura.com`
- Vercel preview and deployment domains

## Deployment

This repository includes a `render.yaml` file for deployment on Render.

### Render deployment checklist

- Push the repository to GitHub
- Create a new Render web service
- Connect the repo and select the service type
- Set required environment variables in Render dashboard
- Deploy the app

## Static Files and Media

The project is configured for:

- static files via WhiteNoise
- media uploads under `/media/`
- optional cloud storage support for AWS S3 using `django-storages`

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py test
python manage.py shell
```

## Contributing

Contributions are welcome. Please follow a standard Git workflow:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a pull request on GitHub.

## License

This project does not currently include a license file. Add one if you want to clarify how others may use the code.

## Support

If you run into issues, open an issue in the GitHub repository or check the project settings and deployment environment variables.

---

Built for Feminine Aura.
