from django.urls import path
from .views import TodosView, TasksView


urlpatterns = [
    path('todos/', TodosView.as_view()),
    path('<int:user_id>/todos/<int:todo_id>/tasks/', TasksView.as_view()),
]
