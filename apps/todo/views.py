from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo
from django.contrib.auth.models import User
from base64 import b64decode
from django.contrib.auth import authenticate


class TodosView(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        pass

class TasksView(View):
    def get(self, request: HttpRequest, user_id: int, todo_id: int) -> HttpRequest:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        todo = user.todos.get(id=todo_id)

        result = []
        for task in todo.tasks.all():
            result.append(model_to_dict(task))
        
        return JsonResponse(result, safe=False)
