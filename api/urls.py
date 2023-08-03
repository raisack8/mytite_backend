# from django.conf.urls import url, include
from django.urls import re_path,include,path
from django.contrib import admin
from api import apis
from .views import StageSectionAPIView

urlpatterns = [
    path('api/', apis.TestApi.as_view(), name = "testapi"),
    # path('stages/', StageSectionAPIView.as_view(), name='stages'),
    path('stages/', apis.StageApi.as_view(), name='stages'),
    path('user_registration/', apis.UserRegistrationApi.as_view(), name='user_registration'),
    path('userinfo_registration/', apis.UserInfoRegistrationApi.as_view(), name='userinfo_registration'),
    path('user_login/', apis.UserLoginApi.as_view(), name='user_login'),
    path('my_section_get/', apis.MySectionGetApi.as_view(), name='my_section_get'),
    path('my_section_add/', apis.MySectionAddApi.as_view(), name='my_section_add'),
    path('my_tite_save/', apis.MyTiteSaveApi.as_view(), name='my_tite_save'),
    path('my_tite_get/', apis.MyTiteGetApi.as_view(), name='my_tite_get'),
    path('section_data_get/', apis.SectionDataGet.as_view(), name='section_data_get'),
    path('section_data_update/', apis.SectionDataUpdate.as_view(), name='section_data_update'),
    
    
    # 付け焼刃
    path('fes_stage_section_return/', apis.AllModelReturn.as_view(), name='section_data_update'),
    path('operate_db_fes_create/', apis.OperateDbFesCreate.as_view(), name='section_data_update'),
    path('operate_db_stage_create/', apis.OperateDbStageCreate.as_view(), name='section_data_update'),
    path('operate_db_section_create/', apis.OperateDbSectionCreate.as_view(), name='section_data_update'),
]