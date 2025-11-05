# Hostel Management Agent Guidelines

## Project Overview
- Django 4.2 project with a single app `booking` providing HTML views and a small DRF API (see `booking/views.py`).
- Templates live under `booking/templates/` and use standard Django templating features.
- REST responses are built with serializers defined in `booking/serializers.py`.

## Environment & Tooling
- Use Python 3.11+ (the CI currently targets Django 4.2 and compatible tooling).
- Install dependencies with `pip install -r requirements.txt`.
- The repo ships `autopep8`/`pycodestyle`; format Python code with `autopep8 --max-line-length 120` and ensure PEP 8 compliance.
- Prefer deterministic dependency additions (pin versions in `requirements.txt`).

## Coding Conventions
- Keep functions and views small; factor shared behavior into helpers inside `booking/` if logic is reused.
- Use Django ORM query optimisations (e.g., `select_related`, `prefetch_related`) when hitting the database inside loops.
- For DRF viewsets, restrict `http_method_names` and rely on serializers for validation.
- Avoid shadowing Django auth helpers (e.g., keep `django.contrib.auth.login` import as `auth_login` if creating a view named `login`).
- Maintain null-safe handling around optional relations like `Guest.room` (see `booking/models.py`).

## Templates
- Keep templates in `booking/templates/`; extend `base.html` if you introduce new pages (create it if needed for shared layout).
- Use `{% url %}` tags for internal links instead of hard-coded paths.
- Pass all context data explicitly from views; do not rely on implicit template variables.

## Tests & Quality
- Add or update tests in `booking/tests.py` when changing behaviour.
- Run `python manage.py test` before committing.
- For API changes, add DRF tests using `APIClient` to cover expected responses.

## Performance & Monitoring
- Respect existing profiling hooks (e.g., `@silk_profile` in `HostelViewSet.list`).
- Avoid N+1 queries when iterating over related models (use aggregation or prefetching).

## Pull Request Expectations
- Summarise key changes and mention affected modules.
- List tests executed (include command invocations).
- Highlight potential migrations and provide execution instructions if you add them.

