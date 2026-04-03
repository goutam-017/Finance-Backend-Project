# Finance Data Processing & Access Control Backend

> Backend Developer Intern Assignment — Django + DRF + SimpleJWT + SQLite

---

## Project Overview

A fully structured REST API backend for a **Finance Dashboard System**.
The backend supports role-based access control, financial record management,
and analytical dashboard summaries.

---

## Tech Stack

| Technology | Purpose | Version |
|---|---|---|
| Python | Core language | Latest |
| Django | Web framework | Latest |
| Django REST Framework | API layer | Latest |
| SimpleJWT | JWT Authentication | Latest |
| django-filter | Query filtering | Latest |
| SQLite | Database | Built-in |

---

## Project Structure

```
finance_backend/
├── manage.py
├── requirements.txt
├── README.md
├── config/          ←  Core config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                    ←  User & auth app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── records/                  ←  Financial records app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── dashboard/                ←  Analytics app
    ├── views.py
    └── urls.py
```

---

## Setup Instructions

### Step 1 — Clone the Repository
```bash
git clone <your-repo-url>
cd finance_backend
```

### Step 2 — Create Virtual Environment
```bash
python -m venv env

env\Scripts\activate        # Windows
source env/bin/activate     # Mac / Linux
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Apply Migrations
```bash
py manage.py makemigrations
py manage.py migrate
```

### Step 5 — Create Admin Superuser
```bash
py manage.py createsuperuser
```
> Follow the prompts to set username, email, and password.
> This user will have **Admin** role and full access.

### Step 6 — Run Development Server
```bash
py manage.py runserver
```
API is now live at: `http://127.0.0.1:8000/api/`

---

## Roles & Permissions

| Role    | View Records | View Dashboard | Create / Update / Delete Records | Manage Users |
|---------|---|---|---|---|
| Viewer  | ✅ | ❌ | ❌ | ❌ |
| Analyst | ✅ | ✅ | ❌ | ❌ |
| Admin   | ✅ | ✅ | ✅ | ✅ |

> New users registered via `/api/register/` are assigned **Viewer** role by default.
> Only an Admin can upgrade roles via `PUT /api/users/<id>/`.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/auth/register/` | Register new user (default role: viewer) | No |
| POST | `/api/auth/login/` | Login and get access + refresh token | No |
| GET | `/api/auth/user_profile/` | Get logged-in user profile | Yes |
| POST | `/api/auth/new_access_token/` | Get new access token using refresh token | No |

---

### User Management _(Admin Only)_

### User Management _(Admin Only)_

| Method | Endpoint | Description |
|---|---|---|
| PUT | `/api/auth/users/<id>/` | Update user info or role |
| PATCH | `/api/auth/users/<id>/` | Partial update user info or role |
| DELETE | `/api/auth/users/<id>/` | Deactivate user (soft delete) |

---

### Financial Records

| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/api/records/` | List records (paginated + filterable) | Viewer+ |
| POST | `/api/records/` | Create a new record | Admin |
| GET | `/api/records/<id>/` | Get a single record by ID | Viewer+ |
| PUT | `/api/records/<id>/` | Full update of a record | Admin |
| PATCH | `/api/records/<id>/` | Partial update of a record | Admin |
| DELETE | `/api/records/<id>/` | Soft delete a record | Admin |

---

### Dashboard Analytics

| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/api/dashboard/summary/` | Full analytics summary | Analyst+ |

---

## Filtering, Search & Pagination

### Query Parameters for `GET /api/records/`

| Parameter | Type | Example | Description |
|---|---|---|---|
| `type` | string | `?type=income` | Filter by `income` or `expense` |
| `category` | string | `?category=salary` | Filter by category (partial match) |
| `date` | date | `?date=2024-01-15` | Filter by exact date |
| `date_from` | date | `?date_from=2024-01-01` | Filter records from this date |
| `date_to` | date | `?date_to=2024-01-31` | Filter records up to this date |
| `search` | string | `?search=food` | Search in category and notes |
| `ordering` | string | `?ordering=-amount` | Sort by `date`, `-date`, `amount`, `-amount` |
| `page` | integer | `?page=2` | Page number for pagination |

> Default page size is **10 records per page**.

### Example Requests
```
GET /api/records/?type=income
GET /api/records/?search=salary&ordering=-date
GET /api/records/?date_from=2024-01-01&date_to=2024-01-31
GET /api/records/?type=expense&category=food&page=2
```

---

## Request & Response Examples

### Register
```json
POST /api/auth/register/

{
    "username": "john",
    "email": "john@gmail.com",
    "password": "john@123",
    "first_name": "John",
    "last_name": "Doe"
}

Response 201:
{
    "msg": "Registration Successfully."
}
```

### Login
```json
POST /api/auth/login/

{
    "username": "john",
    "password": "john@123"
}

Response 200:
{
    "msg": "Login Successfully.",
    "refresh_token": "eyJhbGci...",
    "access_token": "eyJhbGci..."
}
```

### Create Financial Record
```json
POST /api/records/
Authorization: Bearer <admin_access_token>

{
    "amount": 5000.00,
    "type": "income",
    "category": "Salary",
    "date": "2024-01-15",
    "notes": "Monthly salary"
}

Response 201:
{
    "id": 1,
    "amount": "5000.00",
    "type": "income",
    "category": "Salary",
    "date": "2024-01-15",
    "notes": "Monthly salary",
    "created_by": "admin",
    "created_at": "2024-01-15T10:00:00Z"
}
```

### Dashboard Summary
```json
GET /api/dashboard/summary/
Authorization: Bearer <analyst_access_token>

Response 200:
{
    "total_income": 50000.00,
    "total_expense": 20000.00,
    "net_balance": 30000.00,
    "category_totals": [
        { "category": "Salary", "type": "income", "total": 50000.00 },
        { "category": "Food",   "type": "expense", "total": 5000.00 }
    ],
    "monthly_trends": [
        { "month": "2024-01-01", "type": "income", "total": 50000.00 }
    ],
    "weekly_trends": [
        { "week": "2024-01-01", "type": "expense", "total": 1200.00 }
    ],
    "recent_activity": [ "...last 5 records..." ]
}
```

---

## Error Handling & Status Codes

| Status Code | Meaning | When It Occurs |
|---|---|---|
| `200 OK` | Success | GET, PUT, PATCH successful |
| `201 Created` | Resource created | Register or create record |
| `400 Bad Request` | Invalid input | Missing fields, wrong credentials |
| `401 Unauthorized` | No or invalid token | Request without valid access token |
| `403 Forbidden` | Insufficient role | Viewer tries to create a record |
| `404 Not Found` | Resource missing | Record or user ID not found |

---

## Assumptions & Design Decisions

### Assumptions
- New users registered via `/api/auth/register/` are assigned **Viewer** role by default to prevent privilege escalation
- Admin users are created via Django's `createsuperuser` command
- Only Admin can assign or change user roles via `PUT /api/users/<id>/`
- Deactivated users (`is_active=False`) cannot log in even with correct credentials

### Design Decisions

- **Soft Delete** — Both users and records use soft delete. Users have `is_active=False` and records have `is_deleted=True`, preserving all historical data
- **SQLite Database** — Used for simplicity as this is an assessment project. Can be swapped to PostgreSQL by updating `settings.py`
- **JWT Authentication** — Stateless auth using SimpleJWT. Access tokens expire; refresh tokens are used to get new access tokens via `/api/auth/new_access_token/`
- **Role Enforcement** — Custom permission classes (`IsAdmin`, `IsAnalystOrAdmin`, `IsAnyRole`) applied per HTTP method using `get_permissions()`
- **DB-level Aggregation** — Dashboard analytics use Django ORM aggregations (`Sum`, `TruncMonth`, `TruncWeek`) for efficient processing without loading all records into memory
- **Pagination** — `PageNumberPagination` with `page_size=10` applied on all record listings

---

## Optional Features Implemented

| Feature | Status | Details |
|---|---|---|
| JWT Authentication | ✅ Done | Access + Refresh token via SimpleJWT |
| Refresh Token Endpoint | ✅ Done | `POST /api/auth/new_access_token/` |
| Soft Delete (Records) | ✅ Done | `is_deleted` field, data preserved |
| Soft Delete (Users) | ✅ Done | `is_active=False`, login blocked |
| Pagination | ✅ Done | Page size 10, page number based |
| Search Support | ✅ Done | Searches across `category` and `notes` |
| Date Range Filter | ✅ Done | `date_from` and `date_to` params |
| Weekly Trends | ✅ Done | `TruncWeek` aggregation in dashboard |
| Monthly Trends | ✅ Done | `TruncMonth` aggregation in dashboard |

---

## Live Api end points Order

```
Base URL:
https://finance-backend-project-g1f2.onrender.com

Endpoints:
https://finance-backend-project-g1f2.onrender.com/api/auth/register/
https://finance-backend-project-g1f2.onrender.com/api/auth/login/
https://finance-backend-project-g1f2.onrender.com/api/auth/new_access_token/
https://finance-backend-project-g1f2.onrender.com/api/auth/user_profile/
https://finance-backend-project-g1f2.onrender.com/api/auth/users/<id>/

https://finance-backend-project-g1f2.onrender.com/api/records/
https://finance-backend-project-g1f2.onrender.com/api/records/<id>

https://finance-backend-project-g1f2.onrender.com/api/dashboard/summary/
```
```
{
    "username":"admin",
    "password":"admin@123"
}

this is a existing admin user in database.. login through this username and password

```
---