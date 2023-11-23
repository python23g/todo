from django.urls import path
from .views import TodosView , UsersView , UsersDetailsView , TodoDetailsView , TaskView , TasksDetailView


urlpatterns = [
    path('', UsersView.as_view()),
    path('<int:user_id>/', UsersDetailsView.as_view()),
    path('<int:user_id>/todos/', TodosView.as_view()),
    path('<int:user_id>/todos/<int:todo_id>/', TodoDetailsView.as_view()),
    path('<int:user_id>/', UsersDetailsView.as_view()),
    path('<int:user_id>/todos/<int:todo_id>/tasks/', TaskView.as_view()),
    path('<int:user_id>/todos/<int:todo_id>/tasks/<int:task_id>/', TasksDetailView.as_view()),
]
