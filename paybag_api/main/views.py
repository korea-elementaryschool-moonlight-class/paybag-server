from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
import uuid

# Create your views here.
#fields = ['email', 'password', 'phone', 'address', 'count', 'stamp', 'isBlocked', 'uid', 'coupon', 'createdAt', 'updatedAt']

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user(request, pk):
    obj = User.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_phone = data['phone']
        search_password = data['password']
        try :
            obj = User.objects.get(phone=search_phone)
            if search_phone == obj.phone:
                if(obj.password == search_password) :
                    return HttpResponse(status=200)
                else :
                    return HttpResponse(status=400)
            else:
                return HttpResponse(status=400)
        except :
            return HttpResponse(status=400)

@csrf_exempt
def register(request) :
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_name = data['name']
        search_phone = data['phone']
        search_password = data['password']
        search_count = 0
        search_stamp = 0
        search_isBlocked = False
        search_uid = uuid.uuid4()
        search_coupon = 0
        user = User(
            name = search_name,
            password = search_password,
            phone = search_phone,
            count = search_count,
            stamp = search_stamp,
            isBlocked = search_isBlocked,
            uid = search_uid,
            coupon = search_coupon
            )
        user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def market(request) :
    if request.method == 'GET':
        obj = Market.objects.all()
        serializer = MarketSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)