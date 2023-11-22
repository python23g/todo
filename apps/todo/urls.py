from django.urls import path
from .views import TodosView, TasksView, UserView, UsersView


urlpatterns = [
    path('<int:user_id>/todos/', TodosView.as_view()),
    path('<int:user_id>/todos/<int:todo_id>/tasks', TasksView.as_view()),
    path('<int:user_id>', UserView.as_view()),
    path('',UserView.as_view())
]
