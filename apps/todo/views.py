from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo , User , Task
from django.contrib.auth.models import User
import json
from django.core.exceptions import ObjectDoesNotExist

class UsersView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        """get all customers

        Args:
            request (HttpRequest): _description_

        Returns:
            JsonResponse: _description_
        """
        result = []
        for customer in User.objects.all():
            result.append(model_to_dict(customer, fields=['id', 'first_name', 'last_name', 'username']))

        return JsonResponse(result, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:
        """create a new customer

        Args:
            request (HttpRequest): _description_

        Returns:
            JsonResponse: _description_
        """
        data = json.loads(request.body.decode())

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        if all([first_name, last_name, username, password]):
            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )

            return JsonResponse({'message': 'object created.'}, status=201)

        else:
            return JsonResponse({'error': 'invalid data.'}, status=404)


class UsersDetailsView(View):
    def get(self, request: HttpRequest, user_id : int) -> JsonResponse:
        """get customer

        Args:
            request (HttpRequest): _description_
            pk (int): _description_  
        Returns:
            JsonResponse: _description_
        """
        try:
            customer = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'customer does not exist.'}, status=404)
        
        result = model_to_dict(customer, fields=['id', 'first_name', 'last_name', 'username'])
        return JsonResponse(result)

    def put(self, request: HttpRequest, user_id: int) -> JsonResponse:
        """udpate customer

        Args:
            request (HttpRequest): _description_
            pk (int): _description_

        Returns:
            JsonResponse: _description_
        """
        try:
            customer = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'customer does not exist.'}, status=404)

        data = json.loads(request.body.decode())

        customer.first_name = data.get('first_name', customer.first_name)
        customer.last_name = data.get('last_name', customer.last_name)
        customer.username = data.get('username', customer.username)
        customer.password = data.get('password', customer.password)

        customer.save()

        return JsonResponse({'message': 'customer updated.'}, status=203)

    def delete(self, request: HttpRequest, user_id: int) -> JsonResponse:
        """delte customer

        Args:
            request (HttpRequest): _description_
            pk (int): _description_

        Returns:
            JsonResponse: _description_
        """        
        try:
            customer = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'customer does not exist.'}, status=404)

        customer.delete()

        return JsonResponse({'message': 'customer deleted.'}, status=204)


class TodosView(View):
    def get(self, request: HttpRequest, user_id: int) -> HttpRequest:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        todos = Todo.objects.filter(user=user)

        result = []
        for todo in todos:
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)
    
    def post(self, request: HttpRequest,user_id:int) -> JsonResponse:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
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
    def get(self, request: HttpRequest, user_id: int,  todo_id: int) -> JsonResponse:
        try:
            customer = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        
        try:
            customer = Todo.objects.get(id=todo_id)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        
        result = model_to_dict(customer, fields=['id', 'user', 'title', 'created_at'])
        return JsonResponse(result)
    
    def put(self, request: HttpRequest, user_id: int,todo_id: int) -> JsonResponse:
        try:
            customer = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        
        try:
            customer = Todo.objects.get(id=todo_id)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)

        data = json.loads(request.body.decode())

        customer.title = data.get('title', customer.title)

        customer.save()

        return JsonResponse({'message': 'todo updated.'}, status=203)
    
    def delete(self, request: HttpRequest, user_id: int, todo_id: int) -> JsonResponse:
        try:
            customer = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        
        try:
            customer = Todo.objects.get(id=todo_id)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)

        customer.delete()

        return JsonResponse({'message': 'todo deleted.'}, status=204)


class TaskView(View):
    def get(self, request: HttpRequest, user_id: int,todo_id: int) -> HttpRequest:
        try:
            user = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'user does not exist.'}, status=404)
        
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except (ObjectDoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        tasks = Task.objects.filter(todo=todo)
        
        result = []
        for task in tasks:
            result.append(model_to_dict(task))
        
        return JsonResponse(result, safe=False)
    
    def post(self, request: HttpRequest,user_id:int , todo_id: int) -> JsonResponse:
        try:
            user = User.objects.get(id=user_id)
        except (ObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'todo does not exist.'}, status=404)
        
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
    
    
class TasksDetailView(View): 
    def get(self, request: HttpRequest, user_id: int, todo_id: int , task_id: int):
        try:
            user = User.objects.get(id=user_id)
            todo = Todo.objects.get(id=todo_id, user=user)
            task = Task.objects.get(id=task_id , todo=todo)
        except (User.DoesNotExist, Todo.DoesNotExist):
            return JsonResponse({'error': 'user or todo not found.'})

        result = model_to_dict(task , fields=["id" , "todo" , "title" , "description" , "status" , "created_at" , "due_date"])

        return JsonResponse(result, safe=False)
   
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