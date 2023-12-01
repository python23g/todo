from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import User
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
