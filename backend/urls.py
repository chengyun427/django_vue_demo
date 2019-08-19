from django.urls import path

from . import views

urlpatterns = [
    path('testapi', views.testapi, name='testapi'),

    path('listUserMenus', views.listUserMenus, name='listUserMenus'),
    path('getUserByLogin', views.getUserByLogin, name='getUserByLogin'),
]