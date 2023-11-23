from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo, Task
from django.contrib.auth.models import User
import json

class UserView(View):
    def get(self, request: HttpRequest, username: int):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        
        result = []

        result.append(model_to_dict(user))

        return JsonResponse(result, safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body.decode())

        username = data.get('username')
        password = data.get('password')

        user = User.objects.create(username=username, password=password)

        return JsonResponse(model_to_dict(user), safe=False)
    
    def delete(self, request: HttpRequest, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})

        user.delete()

        return JsonResponse({'message': 'User deleted successfully'})
    
class UsersView(View):

    def get(self, request: HttpRequest):

        try:
            user = User.objects.get()
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        
        result = []

        result.append(model_to_dict(user))

        return JsonResponse(result, safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body.decode())

        username = data.get('username')
        password = data.get('password')

        user = User.objects.create(username=username, password=password)

        return JsonResponse(model_to_dict(user), safe=False)
        




class TodosView(View):
    def get(self, request: HttpRequest, user_id: int) -> HttpRequest:
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        todos = Todo.objects.filter(user=user)

        result = []
        for todo in todos:
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)
    
    def post(self, request: HttpRequest, user_id: int):
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        
        data = json.loads(request.body.decode())

        Todo.objects.create(
            title=data.get('title'),
            user=user,
        )

        return JsonResponse({"message": "Created"})

    def put(self, request: HttpRequest, user_id: int, todo_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
        except (User.DoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'user or todo not found.'})
        
        data = json.loads(request.body.decode())
        todo.title = data.get('title', todo.title)
        todo.save()

        return JsonResponse({"message": "Updated"})

    def delete(self, request: HttpRequest, user_id: int, todo_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
        except (User.DoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'user or todo not found.'})
        
        todo.delete()

        return JsonResponse({"message": "Deleted"})


class TasksView(View):
    def get(self, request: HttpRequest, user_id: int, todo_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
        except (User.DoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'user or todo not found.'})

        tasks = Task.objects.filter(todo=todo)
        result = []
        for task in tasks:
            result.append(model_to_dict(task))

        return JsonResponse(result, safe=False)

    def post(self, request: HttpRequest, user_id: int, todo_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
        except (User.DoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'user or todo not found.'})

        data = json.loads(request.body.decode())

        Task.objects.create(
            title=data.get('title'),
            completed=data.get('completed'),
            todo=todo,
        )

        return JsonResponse({"message": "Created"})

    def put(self, request: HttpRequest, user_id: int, todo_id: int, task_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id, todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({'error': 'user, todo, or task not found.'})

        data = json.loads(request.body.decode())
        task.title = data.get('title', task.title)
        task.completed = data.get('completed', task.completed)
        task.save()

        return JsonResponse({"message": "Updated"})

    def delete(self, request: HttpRequest, user_id: int, todo_id: int, task_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id, todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({'error': 'user, todo, or task not found.'})
        
        task.delete()

        return JsonResponse({"message": "Deleted"})
