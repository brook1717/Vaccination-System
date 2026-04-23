<div align="center">

# Vaccination System

**A full-featured vaccination management platform built with Django 5.2 & Django REST Framework**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-ff1709?style=flat&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

</div>

---

## Overview

This system manages the complete vaccination lifecycle — from registering vaccines and centers, to running campaigns, booking time slots with **atomic database transactions**, and exposing data through a **RESTful API** for external frontends.

Built as a real-world demonstration of secure, scalable Django backend architecture.

---

## Table of Contents

- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Author](#author)

---

## Key Features

| Area | Highlights |
|------|-----------|
| **Authentication** | Custom email-based user model, signup, login, POST-only logout, password change & reset, token-based email verification, profile photo upload |
| **Authorization** | `@login_required` on all views, `@staff_member_required` on admin CRUD, `LoginRequiredMixin` & custom `StaffRequiredMixin` on CBVs |
| **Vaccines & Centers** | Full CRUD (staff only), per-center storage tracking with `total_quantity` / `booked_quantity` enforcement |
| **Campaigns** | Browse active campaigns (date-filtered), view only slots with remaining capacity |
| **Booking** | Atomic slot reservation (`select_for_update`), race-condition safe, duplicate-booking prevention, automatic stock decrement |
| **REST API** | Read-only endpoints for centers (with nested stock) and vaccines via Django REST Framework |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| Framework | Django 5.2, Django REST Framework 3.16 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | Custom `AbstractBaseUser` with `PermissionsMixin` |
| Frontend | Django Templates, Bootstrap 5, Font Awesome 5 |
| Media | Pillow for image handling |

---

## Project Structure

```
Vaccination-System/
├── requirements.txt
└── mysite/
    ├── manage.py
    ├── mysite/             # Settings, root URL config
    ├── user/               # Custom User model, auth views, email verification
    ├── vaccine/            # Vaccine model & CRUD views
    ├── center/             # Center & Storage models & CRUD views
    ├── campaign/           # Campaign & Slot models, browsing views
    ├── vaccination/        # Vaccination model, atomic booking logic
    ├── api/                # DRF serializers, read-only API views
    ├── templates/          # Base template & shared components
    └── static/             # CSS, JS, images
```

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip

### 1. Clone & enter the project

```bash
git clone https://github.com/your-username/Vaccination-System.git
cd Vaccination-System
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
cd mysite
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

> You will be prompted for an **email**, **first name**, **last name**, and **password**.  
> This account grants access to the Django Admin panel at `/admin/` and all staff-protected views.

### 6. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## API Reference

All endpoints are **read-only** and served under `/api/`. The browsable API UI is available when `DEBUG=True`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/vaccines/` | List all vaccines |
| `GET` | `/api/vaccines/<id>/` | Retrieve a single vaccine |
| `GET` | `/api/centers/` | List all centers with nested vaccine stock |
| `GET` | `/api/centers/<id>/` | Retrieve a single center with stock details |

<details>
<summary><strong>Example Response</strong> — <code>GET /api/centers/1/</code></summary>

```json
{
  "id": 1,
  "name": "Central Hospital",
  "address": "123 Main St",
  "stock": [
    {
      "id": 1,
      "vaccine": 1,
      "vaccine_name": "Pfizer",
      "total_quantity": 500,
      "booked_quantity": 120,
      "available_quantity": 380
    }
  ]
}
```

</details>

---

## Author

**Biruk Kasahun**  
ALX Software Engineering Graduate  
Backend Developer | Django | REST APIs | Cloud | Security

---

<div align="center">

Contributions, code reviews, and suggestions are welcome.

</div>
