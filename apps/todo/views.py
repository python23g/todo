from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo
from django.contrib.auth.models import User


class TodosView(View):
    def get(self, request: HttpRequest, user_id: int) -> HttpRequest:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})

        result = []
        for todo in user.todos.all():
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)


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
