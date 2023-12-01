from django.urls import path
from .views import UsersView , UsersDetailsView

urlpatterns = [
    path('', UsersView.as_view()),
    path('/', UsersDetailsView.as_view())
    ]
    