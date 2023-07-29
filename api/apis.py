from rest_framework import viewsets, routers
from .models import SectionModel,StageModel,UserModel,MySectionModel
from .serializers import SectionModelSerializer,StageModelSerializer, UserModelSerializer,MySectionModelSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .operates.my_tite import MyTiteGenerator

import datetime
import random
import string
import json
import sys
'''
Django API実装参考URL: https://di-acc2.com/programming/python/10325/
'''

class SectionViewSet(viewsets.ModelViewSet):
    queryset = SectionModel.objects.all()
    serializer_class = SectionModelSerializer

class TestSet(viewsets.ModelViewSet):
    queryset = SectionModel.objects.filter(id=1)
    serializer_class = SectionModelSerializer


class TestApi(ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = SectionModel.objects.filter()
    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SectionModelSerializer
    # 認証
    permission_classes = []
    def get(self, request, *args, **kwargs):
        # リクエストからGETパラメータを取得
        getobj = MyTiteGenerator.get(self, request)
        return Response(getobj)
    
    def post(self, request, *args, **kwargs):
        # POSTリクエストで送信されたデータを取得する
        postobj = MyTiteGenerator.post(self, request)
        return Response(postobj)
        
class StageApi(ListCreateAPIView):
    '''TestApiで取得出来そう'''
    # 対象とするモデルのオブジェクトを定義
    queryset = StageModel.objects.filter()
    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = StageModelSerializer
    # 認証
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # リクエストからGETパラメータを取得
        param_value = request.query_params.get('id')
        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        queryset = StageModel.objects.filter(fes_id=param_value)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class UserRegistrationApi(ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = UserModel.objects.filter()
    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = UserModelSerializer
    # 認証
    permission_classes = []
    # def get(self, request, *args, **kwargs):
    #     # リクエストからGETパラメータを取得
    #     getobj = MyTiteGenerator.get(self, request)
    #     return Response(getobj)
    
    def post(self, request, *args, **kwargs):
        # リクエストからGETパラメータを取得
        user_id = request.data.get('id')
        password = request.data.get('password')
        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        queryset = UserModel.objects.filter(user_id=user_id)
        # ユーザーIDが使われているかどうか
        if len(queryset) != 0:
          return Response({
            "error": "そのログインIDは既に使用されています。別のIDを指定してください。"
            }, status=200)
        serializer = self.serializer_class(queryset, many=True)

        # usernameの為にランダムな英数字を生成「user_XXXXXXXX」
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(8))
        username = 'user_'+random_string

        UserModel.objects.create(
          registration_date=datetime.datetime.today(),
          username=username,
          user_id=user_id,
          password=password,
          active_level=0,
          subscribe_level=0,
          invitation_flg=0,
        )
        user_model = UserModel.objects.get(user_id=user_id)

        return Response({
                "error": "",
                "id": user_model.id,
                "username": username,
            }, status=200)
        

class UserLoginApi(ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = UserModel.objects.filter()
    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = UserModelSerializer
    # 認証
    permission_classes = []
    # def get(self, request, *args, **kwargs):
    #     # リクエストからGETパラメータを取得
    #     getobj = MyTiteGenerator.get(self, request)
    #     return Response(getobj)
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        password = request.data.get('password')
        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        try:
          user_model = UserModel.objects.get(user_id=user_id)
          if user_model.password != password:
            return Response({
              "error": "パスワードが違います。"
              }, status=200)
        except:
          return Response({
            "error": "ログインIDが違います。"
            }, status=200)
        
        return Response({
                "error": "",
                "id": user_model.id,
                "username": user_model.username,
            }, status=200)
    

class MySectionAddApi(ListCreateAPIView):
    queryset = MySectionModel.objects.filter()
    serializer_class = MySectionModelSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        # リクエストからGETパラメータを取得
        fes_id = request.data.get('fesId')
        user_id = request.data.get('userid')

        if user_id == None:
          return Response({
            "error": "予定を追加するにはログインしてください。"
          }, status=200)
        
        # target_date = request.data.get('date')
        start_time = request.data.get('startTime')
        end_time = request.data.get('endTime')
        title = request.data.get('title')
        explain = request.data.get('explain')

        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        try:
          time_split_st = start_time.split(':')
          sp_hour_st = int(time_split_st[0])
          sp_minute_st = int(time_split_st[1])

          time_split_ed = end_time.split(':')
          sp_hour_ed = int(time_split_ed[0])
          sp_minute_ed = int(time_split_ed[1])
          if sp_minute_st % 5 != 0 or sp_minute_ed  % 5 != 0:
            return Response({
              "error": "時間は5分単位で入力してください。"
            }, status=200)
          
          # ★★★懸念：9:00~22:00以外の時間を登録してタイテ作ったらどうなるんだろう
          start_time_dt = datetime.datetime(1899, 12, 30, sp_hour_st, sp_minute_st, 00)
          end_time_dt = datetime.datetime(1899, 12, 30, sp_hour_ed, sp_minute_ed, 00, 0000)
          
          start_time_tz=timezone.datetime(1899, 12, 30, sp_hour_st, sp_minute_st, 00, tzinfo=timezone.utc)
          
          minutes = int((end_time_dt-start_time_dt).total_seconds() / 60)

          MySectionModel.objects.create(
            start_time = start_time_tz,
            allotted_time = minutes,
            title = title,
            other1 = explain,
            fes_id_id = fes_id,
            user_id_id = user_id
          )

        except Exception as e:
          return Response({
            "error": e
            }, status=200)
        
        return Response({
                "error": "",
                "success": "登録が完了しました。"
            }, status=200)
    

# Create your views here.
class HelloView(APIView):
    '''こちらは使わない？'''
    def get(self, request):
      print("++++++++++++")
      get_id = int(request.GET.get("fes_id"))
      # get_obj = SectionModel.objects.filter(fes_id=get_id)
      get_obj = SectionModel.objects.all()
      output_data = serializers.serialize(
        "json",get_obj
        )
      print(output_data)
      return Response(output_data)
      # return HttpResponse(enc,
      #                     content_type="text/json-comment-filtered",
      #                     charset="UTF-8")
    def post(self, request):
      data = request.data
      print("++++++++++++")
      return HttpResponse("{'status':'OK'}",
                          content_type="text/json-comment-filtered",
                          charset='UTF-8')

router = routers.DefaultRouter()
# router.register(r'sections', SectionViewSet)
# router.register(r'test', TestSet)
# router.register(r'api', HelloView)