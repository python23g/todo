from django.views import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
# from django.forms import model_to_dict
import json
from django.db import IntegrityError



class UsersView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        users = User.objects.filter(is_staff=False, is_superuser=False)
        result = []
        for user in users:
            user_dict = {
                "id": user.id,
                "username": user.username
            }
            result.append(user_dict)

        return JsonResponse(result, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body.decode())

        try:
            user = User(username=data['username'])
            user.set_password(raw_password=data['password'])
            user.save()
            
            return JsonResponse({"message": "created."}, status=201)
        except IntegrityError:
            return JsonResponse({'message': 'error'}, status=404)

