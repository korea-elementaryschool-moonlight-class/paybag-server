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
    
    # 로그인
    
    [request]
    {
	    .
        "phone" : "01046156192",
        "password" : "qwer1234"
    }
    [reponse]
    {
    - HttpResponse(200/400)
    }
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
    
    # 회원가입
    
    [request]
    {
	    "name" : "이동준",
        "phone" : "01046156192",
        "password" : "qwer1234"
    }
    [reponse]
    {
    - HttpResponse(200/400)
    }
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

@api_view(['POST'])
@csrf_exempt
def check_market(request) :
    '''

    # 마켓 존재 여부
    
    [request]
    {
	    "eid" : "9518384376747"
    }
    [reponse]
    - HttpResponse(200/400)
    '''

    if request.method == 'POST':
        data = JSONParser().parse(request)
        logging.info("[check_market] " + str(data))
        search_mid = data['mid']
        if Market.objects.filter(mid=search_mid).exists() :
            return HttpResponse(status=200)
        else :
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def market(request) :
    '''
    
    # 전체 마켓 데이터 조회(지도표시)
    
    [request]
    {
	    http://pwnable.co.kr:8000/market/
    }
    [reponse]
    [
        {
            "mid": "market-0001",
            "marketName": "GS25 역삼효성점",
            "count": 11,
            "stock": 13,
            "address": "서울특별시 강남구 역삼동 824-11",
            "latitude": "37.4971584",
            "longitude": "127.0304025",
            "createdAt": "2021-09-17T11:19:54.225150",
            "updatedAt": "2021-09-17T11:19:24",
            "lentcount": 3,
            "returncount": 5
        },
        {
            "mid": "market-0002",
            "marketName": "CU 강남푸르지오점",
            "count": 3,
            "stock": 26,
            "address": "서울 강남구 역삼동 825-20 서울 강남구 테헤란로4길 6",
            "latitude": "37.4976709",
            "longitude": "127.0293410",
            "createdAt": "2021-09-17T11:20:38.516982",
            "updatedAt": "2021-09-17T11:20:34",
            "lentcount": 6,
            "returncount": 1
        },
        {
            "mid": "market-0003",
            "marketName": "CU 역삼디오빌점",
            "count": 2,
            "stock": 5,
            "address": "서울특별시 강남구 역삼동 강남대로84길 33",
            "latitude": "37.4975461",
            "longitude": "127.0310934",
            "createdAt": "2021-09-17T11:21:15.872632",
            "updatedAt": "2021-09-17T11:21:10",
            "lentcount": 5,
            "returncount": 7
        },
        {
            "mid": "market-0004",
            "marketName": "CU 역삼센타점",
            "count": 0,
            "stock": 10,
            "address": "서울 강남구 역삼로9길 28",
            "latitude": "37.4959421",
            "longitude": "127.033803",
            "createdAt": "2021-09-17T18:02:19.178389",
            "updatedAt": "2021-09-17T18:02:17",
            "lentcount": 4,
            "returncount": 1
        },
        ...
        {
            "mid": "market-0014",
            "marketName": "CU 역삼우인점",
            "count": 0,
            "stock": 0,
            "address": "서울 강남구 강남대로84길 8",
            "latitude": "37.4964569",
            "longitude": "127.029314",
            "createdAt": "2021-09-17T18:18:40.473629",
            "updatedAt": "2021-09-17T18:18:27",
            "lentcount": 4,
            "returncount": 10
        }
    ]
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
def market_history_rent(request) :
    '''
    
    # 매장별 대여 기록 조회
    
    [request]
    {
	    http://pwnable.co.kr:8000/market_history_rent/?mid=market-0001
    }
    [reponse]
    [
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8500731947312",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-17T19:06:44.410487",
            "updatedAt": "2021-09-17T19:06:44.391518"
        },
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8984889787721",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-17T19:08:44.612280",
            "updatedAt": "2021-09-17T19:08:44.590913"
        },
        {
            "uid": "b07917d6-8b52-4880-8906-a47e6839cc20",
            "eid": "8500731947312",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "CU 강남푸르지오점",
            "createdAt": "2021-09-17T19:09:33.344940",
            "updatedAt": "2021-09-17T19:09:33.332562"
        }
    ]
    '''
    if request.method == 'GET':
        logging.info("[market_history_rent] " + str(request.GET['mid']))
        search_mid = str(request.GET['mid'])
        obj = History.objects.filter(rentMarket=Market.objects.get(mid=search_mid).marketName)
        serializer = HistorySerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def market_history_return(request) :
    '''
    
    # 매장별 반납 기록 조회
    
    [request]
    {
	    http://pwnable.co.kr:8000/market_history_return/?mid=market-0001
    }
    [reponse]
    [
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8500731947312",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-17T19:06:44.410487",
            "updatedAt": "2021-09-17T19:06:44.391518"
        },
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8984889787721",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-17T19:08:44.612280",
            "updatedAt": "2021-09-17T19:08:44.590913"
        },
        {
            "uid": "b07917d6-8b52-4880-8906-a47e6839cc20",
            "eid": "8984889787721",
            "rentMarket": "CU 역삼디오빌점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-18T04:52:16.517510",
            "updatedAt": "2021-09-18T04:54:26.499895"
        }
    ]
    '''
    if request.method == 'GET':
        logging.info("[market_history_return] " + str(request.GET['mid']))
        search_mid = str(request.GET['mid'])
        obj = History.objects.filter(returnMarket=Market.objects.get(mid=search_mid).marketName)
        serializer = HistorySerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def user(request) :
    '''
    
    # 유저별 데이터 조회
    
    [request]
    {
	    http://pwnable.co.kr:8000/user/?uid=b07917d6-8b52-4880-8906-a47e6839cc20
    }
    [reponse]
    [
        {
            "name": "권태훈",
            "phone": "01052376809",
            "count": 0,
            "stamp": 4,
            "isBlocked": true,
            "uid": "b07917d6-8b52-4880-8906-a47e6839cc20",
            "coupon": 0,
            "createdAt": "2021-09-17T18:43:25.206085",
            "updatedAt": "2021-09-25T16:39:55.213606"
        }
    ]
    '''
    if request.method == 'GET':
        logging.info("[user] " + str(request.GET['uid']))
        search_uid = str(request.GET['uid'])
        obj = User.objects.filter(uid=search_uid)
        serializer = UserSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def history(request) :
    '''
    
    # 유저별 기록 조회
    
    [request]
    {
	    http://pwnable.co.kr:8000/history/?phone=01046156192
    }
    [reponse]
    [
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8500731947312",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-17T19:06:44.410487",
            "updatedAt": "2021-09-17T19:06:44.391518"
        },
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8984889787721",
            "rentMarket": "GS25 역삼효성점",
            "returnMarket": "GS25 역삼효성점",
            "createdAt": "2021-09-17T19:08:44.612280",
            "updatedAt": "2021-09-17T19:08:44.590913"
        },
        {
            "uid": "1007b4e1-d4f6-4b0d-bae2-7b8a2d450fc9",
            "eid": "8984889787721",
            "rentMarket": "CU 역삼디오빌점",
            "returnMarket": "CU 강남푸르지오점",
            "createdAt": "2021-09-17T19:28:01.527003",
            "updatedAt": "2021-09-17T19:28:01.512179"
        }
    ]
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

@api_view(['PUT'])
@csrf_exempt
def block(request) :
    '''
    
    # 유저 정지
    
    [request]
    {
	    "uid" : "b07917d6-8b52-4880-8906-a47e6839cc20",
        "set" : "T",
    }
    [reponse]
    {
    - HttpResponse(200/400)
    }
    '''

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        logging.info("[block] " + str(data))
        search_uid = data['uid']
        search_set = data['set']
        user = User.objects.get(uid = search_uid)
        if(search_set == "T") :
            user.isBlocked = True
        elif(search_set == "F") :
            user.isBlocked = False
        user.updatedAt = timezone.now()
        user.save()
        return HttpResponse(status=200)
    else :
        HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def stock(request) :
    '''
    
    # 마켓별 재고 조회
    
    [request]
    {
	    http://pwnable.co.kr:8000/stock/?mid=market-0012
    }
    [reponse]
    [
        {
            "mid": "market-0012",
            "marketName": "GS25 강남타운점",
            "count": 0,
            "stock": 3,
            "address": "서울 강남구 테헤란로 115",
            "latitude": "37.4990606",
            "longitude": "127.029869",
            "createdAt": "2021-09-17T18:13:06.653247",
            "updatedAt": "2021-09-17T18:12:42",
            "lentcount": 5,
            "returncount": 3
        }
    ]
    '''
    if request.method == 'GET':
        search_mid = str(request.GET['mid'])
        logging.info("[stock] " + str(search_mid))
        obj = Market.objects.filter(mid = search_mid)
        serializer = MarketSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['GET'])
@csrf_exempt
def ecobag_list(request) :
    '''
    
    # 에코백 전체 리스트
    
    [request]
    {
	    NONE
    }
    [reponse]
    [
        {
            "uid": "0",
            "status": "forgot",
            "lastMarket": "GS25 역삼효성점",
            "market": "미정",
            "eid": "9518384376747",
            "note": "0",
            "createdAt": "2021-09-17T19:04:55.403480",
            "updatedAt": "2021-09-25T16:31:56.066648"
        },
        {
            "uid": "0",
            "status": "Having",
            "lastMarket": "GS25 역삼효성점",
            "market": "미정",
            "eid": "8500731947312",
            "note": "0",
            "createdAt": "2021-09-17T19:05:17.878543",
            "updatedAt": "2021-09-17T19:05:11"
        },
        {
            "uid": "미정",
            "status": "Having",
            "lastMarket": "CU 역삼디오빌점",
            "market": "GS25 역삼효성점",
            "eid": "8984889787721",
            "note": "0",
            "createdAt": "2021-09-17T19:05:36.769849",
            "updatedAt": "2021-09-17T19:05:35"
        }
    ]
    '''

    if request.method == 'GET':
        logging.info("[ecobag_list]")
        obj = Ecobag.objects.all()
        serializer = EcobagSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    else :
        HttpResponse(status=400)

@api_view(['POST'])
@csrf_exempt
def market_rent(request) :
    '''
    
    # 에코백 대여
    
    [request]
    {
	    "mid" : "market-0001",
        "phone" : "01052376809",
        "eid" : "8500731947312"
    }
    [reponse]
    {
    - HttpResponse(200/400)
    }
    '''
    if request.method == 'POST':
        data = JSONParser().parse(request)
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


@api_view(['POST'])
@csrf_exempt
def add_lostitem(request) :
    '''

    # 에코백 분실신고
    
    [request]
    {
	    "eid" : "9518384376747"
    }
    [reponse]
    - HttpResponse(200/400)
    '''

    if request.method == 'POST':
        data = JSONParser().parse(request)
        logging.info("[addLostItem] " + str(data))
        search_eid = data['eid']
        ecobag = Ecobag.objects.get(eid=search_eid)
        ecobag.status = "forgot"
        ecobag.updatedAt = timezone.now()
        ecobag.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)






 