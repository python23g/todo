from django.urls import path
from .views import UsersView,UserView


urlpatterns = [
    path('users/', UsersView.as_view()),
    path('user/<int:username>/', UsersView.as_view()),
]

