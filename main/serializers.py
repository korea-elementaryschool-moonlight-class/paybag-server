#serializers.py
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'address', 'count', 'stamp', 'isBlocked', 'uid', 'coupon', 'createdAt', 'updatedAt']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_num', 'valid_thru', 'name', 'cvc', 'card_pw', 'uid', 'createdAt', 'updatedAt']


class EcobagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ecobag
        fields = ['uid', 'status', 'lastMarket', 'market', 'eid', 'note', 'createdAt', 'updatedAt']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['uid', 'eid', 'rentMarket', 'returnMarket', 'createdAt', 'updatedAt']


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['mid', 'marketName', 'count', 'stock', 'address', 'latitude', 'longitude', 'createdAt', 'updatedAt']
