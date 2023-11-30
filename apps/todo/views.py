from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo
from django.contrib.auth.models import User
from base64 import b64decode
from django.contrib.auth import authenticate


class TodosView(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        headers = request.headers

        auth = headers['Authorization']
        token = auth.split(" ")[-1]

        username, password = b64decode(token).decode().split(':')

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'error': 'unauthorized.'}, status=401)

        todos = Todo.objects.filter(user=user)

        result = []
        for todo in todos:
            result.append(model_to_dict(todo))

        return JsonResponse(result, safe=False)


class TasksView(View):
    def get(self, request: HttpRequest, todo_id: int) -> HttpRequest:
        headers = request.headers

        auth = headers['Authorization']
        token = auth.split(" ")[-1]

        username, password = b64decode(token).decode().split(':')

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'error': 'unauthorized.'}, status=401)
        todo = user.todos.get(id=todo_id)

        result = []
        for task in todo.tasks.all():
            result.append(model_to_dict(task))
        
        return JsonResponse(result, safe=False)
