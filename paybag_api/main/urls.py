#urls.py
from django.conf.urls import url, include
from main import views
from django.urls import path


urlpatterns = [
    path('user_list/', views.user_list),
    path('user/<int:pk>/', views.user),
    path('login/', views.login),
    path('register/', views.register),
    path('market/', views.market),
    path('market_rent/', views.market_rent),
    path('market_return/', views.market_return),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]