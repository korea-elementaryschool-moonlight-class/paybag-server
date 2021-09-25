from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from barcode import EAN13
from barcode.writer import ImageWriter
from rest_framework.decorators import api_view
from rest_framework.response import Response
import hashlib
import logging
import random
import shutil
import uuid
from django.utils import timezone
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
    opt ={"font_size": 0, "text_distance": 3, "quiet_zone": 1}
    generate_num = generate_number_user(phone)
    generate_code = EAN13(generate_num, writer=ImageWriter())
    generate_code.save(generate_code, opt)
    locate_user_barcode(generate_code,'.png')
    return str(generate_code)


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

@api_view(['POST'])
@csrf_exempt
def login(request):
    '''
    # Parameters (Requset)
    ---
    ## phone(string) - user phonenumber
    ## password(string) - user password
    ---
    # Parameters (Response)
    ---
    ## name(string) - user name
    HttpResponse(200/400)
    ---
    '''
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_phone = data['phone']
        search_password = data['password']
        encoded_loginPW = search_password.encode()
        encrypted_loginPW = hashlib.sha256(encoded_loginPW).hexdigest()
        logging.info("[login] " + str(data))
        try :
            obj = User.objects.get(phone=search_phone)
            if search_phone == obj.phone:
                if(obj.password == encrypted_loginPW) :
                    obj = User.objects.get(phone=search_phone)
                    dummy_data = {
                        'name' : obj.name,
                        'barcode' : "http://pwnable.co.kr:8000/barcode_user/"+str(obj.barcode_id)+".png",
                        'barcode_id' : str(obj.barcode_id),
                        'phone' : str(obj.phone)
                    }
                    return JsonResponse(dummy_data, status=200)
                else :
                    return HttpResponse(status=400)
            else:
                return HttpResponse(status=400)
        except :
            return HttpResponse(status=400)

@api_view(['POST'])
@csrf_exempt
def register(request) :
    '''
    # Parameters (Requset)
    ---
    ## name(string) - user name
    ## phone(string) - user phonenumber
    ## password(string) - user password
    ---
    # Parameters (Response)
    ---
    HttpResponse(200/400)
    ---
    '''
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_name = data['name']
        search_phone = data['phone']
        search_password = data['password']
        encoded_pw = search_password.encode()
        encrypted_pw = hashlib.sha256(encoded_pw).hexdigest()
        if User.objects.filter(phone=search_phone).exists() :
            return HttpResponse("already exist", status=400)
        else :
            logging.info("[register] " + str(data))
            search_count = 0
            search_stamp = 0
            search_isBlocked = False
            search_uid = uuid.uuid4()
            search_coupon = 0
            user = User(
                name = search_name,
                password = encrypted_pw,
                phone = search_phone,
                count = search_count,
                stamp = search_stamp,
                isBlocked = search_isBlocked,
                uid = search_uid,
                coupon = search_coupon,
                barcode_id = generate_barcode_user_png(search_phone)
            )
            user.save()
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def market(request) :
    '''
    # Parameters (Request)
    ---
    None
    ---
    # Parameters (Response)
    ---
    ## mid(string) - marketid
    ## count(int) - market rent count
    ## stock(int) - market stock count
    ## marketName(string) - market name
    ## address(string) - market address
    ## latitude(string) - market latitude
    ## longitude(stirng) - market longitude
    ## createAt(datetime) - create time
    ## updateAt(datetime) - update time
    ---
    '''
    if request.method == 'GET':
        logging.info("[market] request market data")
        obj = Market.objects.all()
        serializer = MarketSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def history(request) :
    '''
    # Parameters (Request)
    ---
    None
    ---
    # Parameters (Response)
    ---
    ## uid(string) - user unique id
    ## eid(string) - ecobag unique id
    ## rentMarket(string) - rentMarket
    ## returnMarket(string) - returnMarket
    ## createdAt(datetime) - rent datetime
    ## updatedAt(datetime) - return datetime
    ## longitude(stirng) - market longitude
    ---
    '''
    if request.method == 'GET':
        search_phone = request.GET['phone']
        logging.info("[history] " + str(request.GET))
        user = User.objects.get(phone = search_phone)
        obj = History.objects.filter(uid=user.uid)
        serializer = HistorySerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['POST'])
@csrf_exempt
def market_rent(requests) :
    '''
    # Parameters (Request)
    ---
    ## mid(string) - markte unique id
    ## phone(string) - user phone number
    ## eid(string) - ecobag unique id
    ---
    # Parameters (Response)
    ---
    HttpResponse(200/400)
    ---
    '''
    if requests.method == 'POST':
        data = JSONParser().parse(requests)
        print(data)
        search_Mid = data['Mid']
        search_phone = data['phone']
        search_Eid = data['Eid']
        ecobag = Ecobag.objects.get(eid=search_Eid)
        market = Market.objects.get(mid=search_Mid)
        user = User.objects.get(phone=search_phone)
        try :
            history = History.objects.get(uid = user.uid, eid=search_Eid, returnMarket="미정")
            history.returnMarket = market.marketName
            history.updatedAt = timezone.now()
            market.stock = market.stock + 1
            user.count = user.count - 1
            user.updatedAt = timezone.now()
            user.save()
            history.save()
            ecobag.status = "Having"
            ecobag.market  = market.marketName
            ecobag.uid = "미정"
            ecobag.save()
            market.save()
            logging.info("[market_rent] user \"" + str(user.uid) + "\" return \"" + str(search_Eid) + "\" at " + str(market.marketName))
            logging.info("[market_rent] sueccess return")
            return HttpResponse(status=200)
        except :
            ecobag.status = "Renting"
            ecobag.market  = "미정"
            ecobag.uid  = user.uid
            ecobag.lastMarket = market.marketName
            history = History(uid=user.uid, eid=search_Eid, rentMarket=market.marketName, returnMarket="미정", updatedAt=timezone.now())
            if(market.stock > 0) :
                market.count = market.count + 1
                market.stock = market.stock - 1
                user.count = user.count + 1
                user.stamp = user.stamp + 1
                user.updatedAt = timezone.now()
                user.save()
                history.save()
                ecobag.save()
                market.save()
                logging.info("[market_rent] user \"" + str(user.uid) + "\" rent \"" + str(search_Eid) + "\" at " + str(market.marketName)) 
                logging.info("[market_rent] success rent")
                return HttpResponse(status=200)
            else :
                return HttpResponse("no stock :(",status=400)
    else :
        return HttpResponse(status=400)