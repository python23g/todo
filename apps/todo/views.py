from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo , User , Task
from django.contrib.auth.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from base64 import b64decode
from django.contrib.auth import authenticate


class TodosView(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        
        result = []
        todos = Todo.objects.filter(user=user)
        for todo in todos:
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)
    
    def post(self, request: HttpRequest,) -> JsonResponse:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        data = json.loads(request.body.decode())

        title = data.get('title')

        if title:
            Todo.objects.create(
                user=user,
                title=title
            )

            return JsonResponse({'message': 'object created.'}, status=201)

        else:
            return JsonResponse({'error': 'invalid data.'}, status=404)


class TodoDetailsView(View):
    def get(self, request: HttpRequest,  todo_id: int) -> JsonResponse:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        
        try:
            customer = Todo.objects.get(id=todo_id , user = user)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        
        result = model_to_dict(customer, fields=['id', 'user', 'title', 'created_at'])
        return JsonResponse(result)
    
    def put(self, request: HttpRequest,todo_id: int) -> JsonResponse:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        
        try:
            customer = Todo.objects.get(id=todo_id , user = user)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)

        data = json.loads(request.body.decode())

        customer.title = data.get('title', customer.title)

        customer.save()

        return JsonResponse({'message': 'todo updated.'}, status=203)
    
    def delete(self, request: HttpRequest, todo_id: int) -> JsonResponse:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        
        try:
            customer = Todo.objects.get(id=todo_id , user = user)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)

        customer.delete()

        return JsonResponse({'message': 'todo deleted.'}, status=204)


class TaskView(View):
    def get(self, request: HttpRequest,todo_id: int) -> HttpRequest:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        tasks = Task.objects.filter(todo=todo)
        
        result = []
        for task in tasks:
            result.append(model_to_dict(task))
        
        return JsonResponse(result, safe=False)
    
    def post(self, request: HttpRequest, todo_id: int) -> JsonResponse:
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        
        try:
            todo = Todo.objects.get(id=todo_id , user=user)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        data = json.loads(request.body.decode())

        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        due_date = data.get('title')

        if title:
            Task.objects.create(
                todo = todo,
                title = title,
                description = description,
                status = status,
                due_date = due_date
            )

            return JsonResponse({'message': 'object created.'}, status=201)

        else:
            return JsonResponse({'error': 'invalid data.'}, status=404)

    
class TasksDetailView(View): 
    def get(self, request: HttpRequest, todo_id: int , task_id: int):
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id , todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'user or todo not found.'})

        result = model_to_dict(task , fields=["id" , "todo" , "title" , "description" , "status" , "created_at" , "due_date"])

        return JsonResponse(result, safe=False)
   
    def put(self, request: HttpRequest, todo_id: int, task_id: int):
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id, todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({'error': 'user, todo, or task not found.'})

        data = json.loads(request.body.decode())
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.due_date = data.get('due_date', task.due_date)
        task.save()

        return JsonResponse({"message": "Updated"})
    
    def patch(self, request: HttpRequest, todo_id: int, task_id: int):
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id, todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({'error': 'user, todo, or task not found.'})

        data = json.loads(request.body.decode())
        task.status = data.get('status', task.status)
        task.save()

        return JsonResponse({"message": "Updated"})

    def delete(self, request: HttpRequest, todo_id: int, task_id: int):
        header = request.headers
        auth = header["Authorization"][6:]
        username , password = b64decode(auth).decode().split(":")

        user = authenticate(username=username , password=password)
        if user is None:
            return JsonResponse({"erroe": "unauthorized"}, status=401)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id, todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({'error': 'user, todo, or task not found.'})
        
        task.delete()

        return JsonResponse({"message": "Deleted"})