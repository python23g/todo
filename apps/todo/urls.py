from django.urls import path
from .views import TodosView


urlpatterns = [
    path('<int:user_id>/todos/', TodosView.as_view()),
]
