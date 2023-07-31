# from django.conf.urls import url, include
from django.urls import re_path,include,path
from django.contrib import admin
from api import apis
from .views import StageSectionAPIView

urlpatterns = [
    path('api/', apis.TestApi.as_view(), name = "testapi"),
    path('hello/', apis.HelloView.as_view()),
    # path('stages/', StageSectionAPIView.as_view(), name='stages'),
    path('stages/', apis.StageApi.as_view(), name='stages'),
    path('user_registration/', apis.UserRegistrationApi.as_view(), name='user_registration'),
    path('user_login/', apis.UserLoginApi.as_view(), name='user_login'),
    path('my_section_get/', apis.MySectionGetApi.as_view(), name='my_section_get'),
    path('my_section_add/', apis.MySectionAddApi.as_view(), name='my_section_add'),
    path('my_tite_save/', apis.MyTiteSaveApi.as_view(), name='my_tite_save'),
]