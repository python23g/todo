from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import User
import json


class UsersView(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        users = User.objects.filter(is_staff=False, is_active=True, is_superuser=False)
        result = []
        for user in users:
            result.append(model_to_dict(user))
        return JsonResponse(result, safe=False)
    
    def post(self, request: HttpRequest) -> HttpRequest:
        data=json.loads(request.body.decode())
        user=User.objects.create(
            user=user,
            pricture=data.get('pricture'),
            phone = data.get('phone'),
            date_of_birth = data.get("date_of_birth")
        )


class UsersItemView(View):
    def get(sef, request: HttpRequest, pk:int):
        user=User.objects.get(id=pk)
        result=model_to_dict(user)
        return JsonResponse(result, safe=False)
