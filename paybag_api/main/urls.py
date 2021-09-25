#urls.py
from django.conf.urls import url, include
from main import views
from django.urls import path


urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('history/', views.history),
    path('market/', views.market),
    path('market_rent/', views.market_rent),
    path('stock/', views.stock),
    path('check_market/', views.check_market),
    path('market_history_return/', views.market_history_return),
    path('market_history_rent/', views.market_history_rent),
    path('block/', views.block),
    path('user/', views.user),
    path('add_lostitem/', views.add_lostitem),
    path('ecobag_list/', views.ecobag_list),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]