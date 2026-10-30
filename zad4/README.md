# zad4 – Katalog gier (Django + fetch())

Python 3.12, Django 6.x (działa też na 5.x).

    python -m venv .venv
    # Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
    python -m pip install -r requirements.txt
    python manage.py migrate
    python manage.py loaddata gry        # 8 przykładowych gier
    python manage.py createsuperuser     # opcjonalnie, do /admin/
    python manage.py runserver

- Strona główna: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/gry/
- Filtry: /api/gry/?wieloosobowa=true , /api/gry/?gatunek=rpg
- Admin: http://127.0.0.1:8000/admin/
