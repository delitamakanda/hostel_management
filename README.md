# Hostel Management

[![Hostel Management CI](https://github.com/delitamakanda/hostel_management/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/delitamakanda/hostel_management/actions/workflows/ci.yml)

A Django-based hostel management system that streamlines how residents, rooms, and hostels are organised. It offers HTML views for common guest workflows as well as a small REST API for fetching hostel data.

## Features

- **Guest onboarding** – Sign up, edit guest profiles, and persist personal information such as contact details and enrolment numbers.
- **Room allocation** – Allow guests to select an available room based on their gender and booking preferences. Occupancy is tracked automatically when a room is selected or released.
- **Hostel catalogue** – Maintain metadata for each hostel including its warden, caretaker, and supported room types.
- **REST API** – Query the list of hostels via `/api/hostels/` with optional case-insensitive filtering by name.

## Requirements

- Python 3.11+
- Django 4.2 (pinned in `requirements.txt`)
- SQLite (bundled with Python, used by default via Django)

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/delitamakanda/hostel_management.git
   cd hostel_management
   ```
2. **Create and activate a virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (optional, for Django admin access)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Development Server

Start the Django development server locally:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the web interface. The Django admin is available at `http://127.0.0.1:8000/admin/` for users with staff privileges.

## Using the API

The project exposes a read-only endpoint for hostels through Django REST Framework:

```http
GET /api/hostels/
GET /api/hostels/?name=Sunrise
```

Responses return JSON encoded hostel objects, and the `name` query parameter allows case-insensitive partial matching.

## Running Tests

Execute the built-in unit tests before submitting changes:

```bash
python manage.py test
```

## Project Structure

```
booking/            # Core Django app containing models, forms, serializers, views, and templates
hostelmanagement/   # Project configuration (settings, URLs, WSGI/ASGI entrypoints)
manage.py           # Django management script
requirements.txt    # Python dependencies
```

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes following the project's coding standards.
3. Run the test suite (`python manage.py test`).
4. Submit a pull request with a clear summary of your updates and any additional setup steps.

---

For additional questions or improvements, please open an issue in the repository.
