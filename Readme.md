# paybag-server
## Install
- 1. `pip install -r requirments.txt` 
- 2. `python3 paybag_api/manage.py runserver`
- 3.  go to website http://127.0.0.01:8000/swagger/

## Api-list
- show in http://pwnable.co.kr:8000/swagger/
- /add_lostitem/
```
에코백 분실신고
[request]
{
    "eid" : "9518384376747"
}
[reponse]
- HttpResponse(200/400)
```
- /block/
```
유저 정지
[request]
{
    "uid" : "b07917d6-8b52-4880-8906-a47e6839cc20",
    "set" : "T",
}
[reponse]
{
- HttpResponse(200/400)
}
```
- /check_market/
```
마켓 존재 여부
[request]
{
    "eid" : "9518384376747"
}
[reponse]
- HttpResponse(200/400)
```
- /ecobag_list/
```
에코백 전체 리스트
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
```
- /history/
```
유저별 기록 조회
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
```
- /login/
```
로그인
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
```
- /market/
```
전체 마켓 데이터 조회(지도 표시)
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
```
- /market_history_rent/
```
매장별 대여 기록 조회
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
```
- /market_history_return/
```
매장별 반납 기록 조회
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
```
- /market_rent/
```
에코백 대여
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
```
- /register/
```
회원가입
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
```
- /stock/
```
마켓별 재고 조회
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
```
- /user/
```
유저별 데이터 조회
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
```
