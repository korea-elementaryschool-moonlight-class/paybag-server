from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from barcode import EAN13
from barcode.writer import ImageWriter
import random
import shutil
import uuid
import datetime

src = './'
dir_u = './barcode_user/'

def generate_number_user(phone) -> str:
    generate_number = phone
    generate_number += str(random.randrange(0,10)) + str(random.randrange(0,10))
    return generate_number

#Move User barcode
def locate_user_barcode(generate_code,type):
    filename = str(generate_code) + type
    shutil.move(src+filename,dir_u+filename)

#Generate barcode for User
def generate_barcode_user_png(phone) -> str:
    generate_num = generate_number_user(phone)
    generate_code = EAN13(generate_num, writer=ImageWriter())
    generate_code.save(generate_code)
    locate_user_barcode(generate_code,'.png')
    return str(generate_code)

#Generate barcode for User
def generate_barcode_user_svg(phone) -> str:
    generate_num = generate_number_user(phone)
    generate_code = EAN13(generate_num)
    generate_code.save(generate_code)
    locate_user_barcode(generate_code,'.svg')
    return str(generate_code)

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
        generate_barcode_user_png(search_phone)
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

@csrf_exempt
def market_rent(requests) :
    if requests.method == 'POST':
        data = JSONParser().parse(requests)
        search_Mid = data['Mid']
        search_phone = data['phone']
        search_Eid = data['Eid']
        ecobag = Ecobag.objects.get(eid=search_Eid)
        market = Market.objects.get(mid=search_Mid)
        user = User.objects.get(phone=search_phone)
        ecobag.status = "Renting"
        ecobag.lastMarket = market.marketName
        history = History(uid=user.uid, eid=search_Eid, rentMarket=market.marketName, returnMarket="0", updatedAt=datetime.datetime.now())
        market.count = market.count + 1
        market.stock = market.stock - 1
        user.count = user.count + 1
        user.stamp = user.stamp + 1
        user.updatedAt = datetime.datetime.now()
        user.save()
        history.save()
        ecobag.save()
        market.save()
        return HttpResponse(status=200)
    else :
        return HttpResponse(status=400)

@csrf_exempt
def market_return(requests) :
    if requests.method == 'POST':
        data = JSONParser().parse(requests)
        search_Mid = data['Mid']
        search_phone = data['phone']
        search_Eid = data['Eid']
        ecobag = Ecobag.objects.get(eid=search_Eid)
        market = Market.objects.get(mid=search_Mid)
        user = User.objects.get(phone=search_phone)
        ecobag.status = "Having"
        ecobag.market = market.marketName
        history = History.objects.get(uid = user.uid, eid=search_Eid, returnMarket="0")
        history.returnMarket = market.marketName
        market.stock = market.stock + 1
        user.count = user.count - 1
        user.updatedAt = datetime.datetime.now()
        user.save()
        history.save()
        ecobag.save()
        market.save()
        return HttpResponse(status=200)
    else :
        return HttpResponse(status=400)