from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/tasks/", views.task_list, name="task-list"),
    path("api/tasks/<int:task_id>/", views.task_detail, name="task-detail"),
]
