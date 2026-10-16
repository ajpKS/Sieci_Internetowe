import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .models import Task

MAX_TITLE_LENGTH = Task._meta.get_field("title").max_length


def error(message, status):
    return JsonResponse({"error": message}, status=status)


def parse_json_body(request):
    """Return the decoded JSON object from the request, or None if invalid."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


@ensure_csrf_cookie
def index(request):
    """Serves the page and makes sure the CSRF cookie is set for fetch()."""
    return render(request, "tasks/index.html")


@require_http_methods(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        return JsonResponse([t.to_dict() for t in Task.objects.all()], safe=False)

    data = parse_json_body(request)
    if data is None:
        return error("Nieprawidłowy format JSON.", 400)

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return error("Treść zadania nie może być pusta.", 400)
    title = title.strip()
    if len(title) > MAX_TITLE_LENGTH:
        return error(f"Treść zadania może mieć maksymalnie {MAX_TITLE_LENGTH} znaków.", 400)

    task = Task.objects.create(title=title)
    return JsonResponse(task.to_dict(), status=201)


@require_http_methods(["PATCH", "DELETE"])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return error("Zadanie o podanym ID nie istnieje.", 404)

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"deleted": task_id})

    data = parse_json_body(request)
    if data is None:
        return error("Nieprawidłowy format JSON.", 400)
    if not isinstance(data.get("completed"), bool):
        return error("Pole 'completed' musi mieć wartość true lub false.", 400)

    task.completed = data["completed"]
    task.save(update_fields=["completed"])
    return JsonResponse(task.to_dict())
