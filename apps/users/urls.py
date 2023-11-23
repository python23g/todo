from django.urls import path
from .views import UsersView, UsersItemView


urlpatterns = [
    path('', UsersView.as_view()),
    path('<int:pk>', UsersItemView.as_view())
]
