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
    