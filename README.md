# Lost & Found Network

**Lost & Found Network** is a full-stack Django web application that helps people report, discover, and resolve lost and found items through a structured matching workflow.

The platform combines a server-rendered web application with a REST API, user authentication, API-key access, report management, automated matching, match confirmation, reviews, filtering, pagination, and production deployment.

**Live Demo:** https://lostfoundnetwork-production.up.railway.app/

**Repository:** https://github.com/raheelhassangit/Lost_Found_Network

---

## What Problem Does It Solve?

Traditional lost-and-found processes often depend on manually searching through posts or contacting people individually.

Lost & Found Network provides a centralized workflow where users can:

1. Create an account.
2. Report a lost or found item.
3. Browse and search existing reports.
4. Automatically identify potential matches.
5. Review potential matches.
6. Confirm a match from both sides.
7. Resolve the related reports.
8. Leave feedback about the resolution.

The goal is to turn a simple lost-and-found website into a structured application with real backend workflows and API capabilities.

---

## Core Features

### User Authentication

* User registration
* Login and logout
* Custom user model
* Email-based password reset
* Password validation
* Optional phone number
* Session-based authentication

### Lost & Found Reports

Users can create reports containing:

* Report type — Lost / Found
* Item name
* Description
* Category
* Color
* Location
* Date lost/found
* Item image
* Report status

Reports can be:

* Created
* Viewed
* Updated
* Deleted
* Marked as processing
* Closed/resolved

---

## Intelligent Matching

The application includes an automated matching system located in:

```text
reports/matching.py
```

When a report is created, a background task evaluates it against relevant reports of the opposite type.

For example:

```text
Lost Phone
     │
     ▼
New Lost Report
     │
     ▼
Matching Task
     │
     ├── Category
     ├── Location
     ├── Date
     ├── Color
     └── Description similarity
     │
     ▼
Match Score
     │
     ▼
Potential Matches
```

### Current Matching Score

The current scoring system considers several signals:

| Signal                   | Maximum Score |
| ------------------------ | ------------: |
| Same category            |            30 |
| Same/related location    |            25 |
| Date proximity           |            20 |
| Same color               |            15 |
| Description word overlap |            10 |
| **Maximum**              |       **100** |

A match is created when the calculated score reaches the configured threshold.

```python
MATCH_THRESHOLD = 40
```

The matching logic also creates a reverse match so that both sides can see the relationship.

---

## Match Confirmation Workflow

A potential match does not immediately resolve a report.

Both sides must confirm the match.

```text
Potential Match
      │
      ▼
User A confirms
      │
      ▼
Waiting for User B
      │
      ▼
User B confirms
      │
      ▼
Both sides confirmed
      │
      ├── Reports → CLOSED
      └── Reviews → Created
```

This prevents one user from unilaterally marking another person's report as resolved.

---

## Review System

Once a report is resolved, the system can create a review associated with the report.

Reviews contain:

* Reviewer
* Report
* Comment
* Creation timestamp

The application also supports platform testimonials with:

* 1–5 star rating
* Comment
* User
* Timestamp

---

# REST API

The application exposes a REST API through **Django REST Framework**.

API routes are organized under:

```text
/api/
```

The API uses Django REST Framework's `DefaultRouter` for resource endpoints.

### Available API Resources

```text
/api/reports/
/api/categories/
/api/reviews/
/api/matches/
/api/testimonials/
```

Authentication endpoints are also available:

```text
/api/token/
/api/token/refresh/
```

---

## API Authentication

The API supports multiple authentication mechanisms:

* API Key authentication
* JWT authentication
* Django session authentication

### API Key

Users can generate API keys from the application.

API keys support scopes:

```text
reports
testimonials
matches
all
```

Requests using an API key send it through the:

```http
X-API-Key
```

header.

Example:

```http
GET /api/reports/
X-API-Key: YOUR_API_KEY
```

API keys also track:

* Label
* Creation time
* Last-used time
* Active/inactive status
* Access scope

Keys can be revoked without deleting the user account.

---

## JWT Authentication

The application uses `djangorestframework-simplejwt` for token-based authentication.

Token endpoints:

```text
POST /api/token/
POST /api/token/refresh/
```

This allows external clients to authenticate with the API independently from the server-rendered web interface.

---

# API Features

The REST API includes:

### Filtering

Reports can be filtered by:

* Report type
* Status
* Category

### Searching

Search is supported across:

* Item name
* Description
* Location

### Ordering

Reports can be ordered using:

* Date
* Creation date

### Pagination

API results use page-number pagination.

The default page size is:

```text
9
```

### Throttling

The API includes anonymous and authenticated request throttling.

```text
Anonymous: 20 requests/minute
Authenticated: 100 requests/minute
```

---

# Authorization

The project separates authentication from authorization.

For report operations, users are restricted from modifying reports belonging to other users.

The project includes:

```text
IsOwnerOrReadOnly
```

which allows:

* Public read access where appropriate
* Modification only by the report owner

API keys also have scope-based permissions through:

```text
HasAPIKeyScope
```

This provides more granular control over programmatic API access.

---

# Application Architecture

The project is divided into focused Django applications.

```text
                    ┌─────────────────────┐
                    │       Browser       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Django        │
                    │   Web Application   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         Accounts           Reports            Core
              │                │                │
              │                ▼                │
              │          Matching System        │
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Database      │
                    │        MySQL        │
                    └─────────────────────┘

                    ┌─────────────────────┐
                    │     REST API        │
                    │ Django REST         │
                    │ Framework           │
                    └─────────────────────┘
```

---

# Django Applications

## `accounts`

Responsible for:

* Custom user model
* Registration
* Login/logout integration
* Password reset
* API keys
* API key authentication
* API key scope permissions

Important files:

```text
accounts/
├── authentication.py
├── forms.py
├── models.py
├── permissions.py
├── views.py
└── urls.py
```

---

## `reports`

The main business-logic application.

Responsible for:

* Categories
* Lost reports
* Found reports
* Matching
* Match confirmation
* Reviews
* Report lifecycle
* Report permissions
* Report API endpoints

Important files:

```text
reports/
├── models.py
├── matching.py
├── forms.py
├── serializers.py
├── permissions.py
├── views.py
├── api_views.py
└── urls.py
```

---

## `core`

Handles platform-level functionality such as:

* Homepage
* Testimonials
* Support page
* Privacy page
* Terms page
* API key management page
* API token display

---

## `api`

Provides the central API routing layer.

It registers the application's DRF ViewSets:

```text
Reports
Categories
Reviews
Matches
Testimonials
```

and exposes JWT token endpoints.

---

## `config`

Contains the Django project configuration:

```text
config/
├── settings.py
├── urls.py
├── asgi.py
└── wsgi.py
```

The project configuration includes separate production-oriented settings for:

* Environment variables
* Security
* Static files
* Media files
* Database
* CORS
* CSRF trusted origins
* REST framework
* Authentication
* API throttling

---

# Project Structure

```text
Lost_Found_Network/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   ├── authentication.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
│
├── api/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── templates/
│   │   └── core/
│   ├── templatetags/
│   ├── api_views.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── reports/
│   ├── migrations/
│   ├── templates/
│   │   └── reports/
│   ├── api_views.py
│   ├── forms.py
│   ├── matching.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   └── views.py
│
├── theme/
│   ├── static/
│   ├── static_src/
│   └── templates/
│
├── manage.py
├── Procfile
├── requirements.txt
└── README.md
```

---

# Frontend

The project uses Django Templates for server-rendered pages with Tailwind CSS for styling.

The application includes dedicated interfaces for:

* Homepage
* Authentication
* Password reset
* Report listing
* Report creation
* Report details
* Report editing
* Report deletion
* My Reports
* My Matches
* Match confirmation
* Report resolution
* API key management
* Testimonials
* Support
* Privacy
* Terms

The Tailwind output is stored under:

```text
theme/static/css/dist/
```

---

# Media & Images

Report images are supported through Django's `ImageField`.

The production configuration uses **Cloudinary** for media storage.

This separates uploaded media from the application server and makes image handling suitable for a deployed environment.

---

# Database

The current project uses:

```text
MySQL
```

Database configuration is loaded through environment variables rather than hard-coded credentials.

Required database configuration includes:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

---

# Production Deployment

The application is deployed on **Railway**.

Production uses:

```text
Gunicorn
```

with Django's WSGI application:

```text
config.wsgi
```

The repository contains a `Procfile` with:

```text
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

The release process automatically runs Django migrations during deployment.

---

# Production Static Files

Static files are configured using **WhiteNoise** with compressed manifest storage.

Production configuration includes:

```text
WhiteNoise
CompressedManifestStaticFilesStorage
```

This allows the Django application to serve its collected static assets in the deployed environment.

---

# Security Configuration

The production configuration includes several Django security features.

When `DEBUG=False`, the application enables:

* Secure session cookies
* Secure CSRF cookies
* HSTS
* HSTS subdomains
* Environment-based secret key
* Configurable allowed hosts
* Configurable CSRF trusted origins
* Configurable CORS origins

Secrets and deployment-specific configuration are loaded using environment variables.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/raheelhassangit/Lost_Found_Network.git

cd Lost_Found_Network
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file and configure the required settings.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=lost_found
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

For production, configure the required Cloudinary, email, CORS, CSRF, and database variables as well.

## 5. Run migrations

```bash
python manage.py migrate
```

## 6. Create an administrator

```bash
python manage.py createsuperuser
```

## 7. Start the server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# Environment Variables

The application reads configuration from environment variables using `python-decouple`.

Common configuration includes:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS

DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

CORS_ALLOWED_ORIGINS
CSRF_TRUSTED_ORIGINS

EMAIL_BACKEND
EMAIL_HOST
EMAIL_PORT
EMAIL_USE_TLS
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL

PLATFORM_SUPPORT_EMAIL

CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
```

Never commit production secrets or credentials to the repository.

---

# Technology Stack

| Area              | Technology                   |
| ----------------- | ---------------------------- |
| Language          | Python                       |
| Web Framework     | Django                       |
| API Framework     | Django REST Framework        |
| Authentication    | Django Auth + JWT + API Keys |
| Database          | MySQL                        |
| Filtering         | django-filter                |
| API Search        | DRF SearchFilter             |
| API Ordering      | DRF OrderingFilter           |
| API Pagination    | PageNumberPagination         |
| API Throttling    | DRF throttling               |
| Frontend          | Django Templates             |
| CSS               | Tailwind CSS                 |
| Image Processing  | Pillow                       |
| Media Storage     | Cloudinary                   |
| Static Files      | WhiteNoise                   |
| Production Server | Gunicorn                     |
| Deployment        | Railway                      |

---

# Future Development

The current matching system provides a foundation for more advanced item matching.

Potential improvements include:

* Semantic text similarity
* Embedding-based matching
* Machine-learning match scoring
* Better candidate ranking
* Image similarity
* Dedicated ML inference service with FastAPI
* Background processing with Celery
* Redis-based caching
* Match notifications
* Automated test coverage
* API documentation
* CI/CD
* Monitoring and health checks

The matching architecture is intentionally separated into `reports/matching.py`, making it possible to evolve the scoring system without redesigning the complete reporting workflow.

---

# Open Source

Lost & Found Network is open-source software released under the MIT License.

You are free to use, modify, study, and distribute the project according to the terms of the license.

Contributions, bug reports, feature requests, and improvements are welcome.

---

# Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application locally.
5. Commit your changes.
6. Open a Pull Request.

For larger changes, consider opening an issue first to discuss the proposed implementation.

---

# Author

**Raheel Hassan**

BS Information Technology
University of the Punjab

GitHub: https://github.com/raheelhassangit

LinkedIn: https://www.linkedin.com/in/raheel-hassan/

---

# License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.
