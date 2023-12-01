from django.urls import path
from .views import TodosView , TodoDetailsView , TaskView , TasksDetailView


urlpatterns = [
    path('todos/', TodosView.as_view()),
    path('todos/<int:todo_id>/', TodoDetailsView.as_view()),
    path('todos/<int:todo_id>/tasks/', TaskView.as_view()),
    path('todos/<int:todo_id>/tasks/<int:task_id>/', TasksDetailView.as_view()),
]