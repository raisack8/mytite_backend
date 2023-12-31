from rest_framework import viewsets, routers
from .models import SectionModel,StageModel,UserModel,MySectionModel,MyTiteModel,FesModel
from .serializers import SectionModelSerializer,StageModelSerializer, UserModelSerializer,MySectionModelSerializer,MyTiteModelSerializer,FesModelSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .operates.my_tite import MyTiteGenerator
from .operates.my_tite_get import MyTiteGeneratorFromSlot

# import datetime
from datetime import datetime, timedelta
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
          registration_date=datetime.today(),
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
        
class UserInfoRegistrationApi(ListCreateAPIView):
    queryset = UserModel.objects.filter()
    serializer_class = UserModelSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        # リクエストからGETパラメータを取得
        print("=== UserInfoRegistrationApi")
        user_id = request.data.get('id')
        username = request.data.get('username')
        change_flag = request.data.get('change_flag')
        print(change_flag)
        if not change_flag:
          return Response({
                "error": "",
                "id": user_id,
                "username": '',
            }, status=200)
        # ユーザー名が既に存在していないか
        queryset = UserModel.objects.filter(username=username)
        if len(queryset) != 0:
          return Response({
            "error": "そのユーザー名は既に使用されています。別のユーザー名を指定してください。"
            }, status=200)

        # ユーザー名が使われていなかったらDBを更新する
        user_model = UserModel.objects.get(id=user_id)
        user_model.username = username
        user_model.save()

        return Response({
                "error": "",
                "id": user_model.id,
                "username": username,
            }, status=200)
        

class UserLoginApi(ListCreateAPIView):
    queryset = UserModel.objects.filter()
    serializer_class = UserModelSerializer
    permission_classes = []
    
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
        
        my_tite_model = MyTiteModel.objects.filter(
           user_id_id = user_model.id
        )
        mytite_id_list = [obj.id for obj in my_tite_model]

        return Response({
                "error": "",
                "id": user_model.id,
                "username": user_model.username,
                "mytitelist":mytite_id_list
            }, status=200)
    
class MySectionGetApi(ListCreateAPIView):
    queryset = MySectionModel.objects.filter()
    serializer_class = MySectionModelSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        my_sec_list = request.data.get('my_sec_list')
        if my_sec_list == '':
            # my_secが登録されていなかったら
            return Response({
                "error": "",
                "data":{}
            }, status=200)
        
        parse_list = json.loads(f"[{my_sec_list}]")
        queryset = MySectionModel.objects.filter(id__in=parse_list)

        obj_list = []

        for query in queryset:
            
            end_time = query.start_time + timedelta(minutes=query.allotted_time)
            # start_timeとend_timeを指定された形式に変換する
            start_time_str = query.start_time.strftime('%H:%M')  # '12:30'となる
            end_time_str = end_time.strftime('%H:%M')  # '14:30'となる

            obj={
              'id':query.id,
              'create_date':query.create_date,
              'start_time':query.start_time,
              'allotted_time':query.allotted_time,
              'display_start_time': start_time_str,
              'display_end_time': end_time_str,
              # stage_idを仮指定
              'title':query.title,
              'other1':query.other1,
              'other2':query.other2,
              }
            obj_list.append(obj)

        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        return Response({
                "error": "",
                "data": obj_list
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
        start_time_hour = request.data.get('startTimeHour')
        start_time_minute = request.data.get('startTimeMinute')
        end_time_hour = request.data.get('endTimeHour')
        end_time_minute = request.data.get('endTimeMinute')
        title = request.data.get('title')
        explain = request.data.get('explain')

        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        sp_hour_st = int(start_time_hour)
        sp_minute_st = int(start_time_minute)

        sp_hour_ed = int(end_time_hour)
        sp_minute_ed = int(end_time_minute)
        if sp_minute_st % 5 != 0 or sp_minute_ed  % 5 != 0:
          return Response({
            "error": "時間は5分単位で入力してください。"
          }, status=200)
        
        # ★★★懸念：9:00~22:00以外の時間を登録してタイテ作ったらどうなるんだろう
        start_time_dt = datetime(1899, 12, 30, sp_hour_st, sp_minute_st, 00, 0000)
        end_time_dt = datetime(1899, 12, 30, sp_hour_ed, sp_minute_ed, 00, 0000)
        
        start_time_tz=timezone.datetime(1899, 12, 30, sp_hour_st, sp_minute_st, 00, tzinfo=timezone.utc)
        
        minutes = int((end_time_dt-start_time_dt).total_seconds() / 60)
        if minutes < 10:
          return Response({
            "error": "予定は必ず10分以上としてください"
          }, status=200)

        my_section_model = MySectionModel.objects.create(
          start_time = start_time_tz,
          allotted_time = minutes,
          title = title,
          other1 = explain,
          other2 = '',
          fes_id_id = fes_id,
          user_id_id = user_id
        )

        return Response({
                "error": "",
                "success": "登録が完了しました。",
                "data": my_section_model.id
            }, status=200)
    
class MyTiteSaveApi(ListCreateAPIView):
    queryset = MyTiteModel.objects.filter()
    serializer_class = MyTiteModelSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        # リクエストからGETパラメータを取得
        user_id = request.data['user_id']
        sec_list = request.data['sec_list']
        my_sec_list = request.data['my_sec_list']
        if len(sec_list)==0 and len(my_sec_list)==0:
          return Response({
              "error": "申し訳ありませんが、フェスのアーティスト選択画面に戻って再度みたいアーティストを選択し直してください。"
            }, status=200)

        my_tite_model = MyTiteModel.objects.filter(
           user_id_id = user_id
        )
        if len(my_tite_model)>=5:
          return Response({
              "error": "保存できるマイタイテの数を超えています。"
            }, status=200)
        
        created_model = MyTiteModel.objects.create(
            section_list = request.data['sec_list'],
            my_section_list = request.data['my_sec_list'],
            slot_num = 0,
            title = '',
            explain = '',
            user_id_id = user_id,
            fes_id_id = request.data['fes_id'],
          )

        return Response({
                "error": "",
                "success": "登録が完了しました。",
                "modelid": created_model.id
            }, status=200)

class MyTiteGetApi(ListCreateAPIView):
    queryset = MyTiteModel.objects.filter()
    serializer_class = MyTiteModelSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        # POSTリクエストで送信されたデータを取得する
        postobj = MyTiteGeneratorFromSlot.post(self, request)
        return Response(postobj)

class SectionDataGet(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        # POSTリクエストで送信されたデータを取得する
        section_model = SectionModel.objects.get(id=request.data["id"])
        print(section_model.id)
        obj = {
          'id': section_model.id,
          'appearance_date': section_model.appearance_date,
          'start_time': section_model.start_time,
          'allotted_time': section_model.allotted_time,
          'artist_name': section_model.artist_name,
          'change_time_flg': section_model.change_time_flg,
          'other1': section_model.other1,
          'other2': section_model.other2,
          'other3': section_model.other3,
          'other4': section_model.other4,
          'other5': section_model.other5,
          'official_url': section_model.official_url,
          'twitter_id': section_model.twitter_id,
          'insta_id': section_model.insta_id,
          'fes_id_id': section_model.fes_id_id,
          'live_category_id': section_model.live_category_id,
          'stage_id': section_model.stage_id,
          'apparence_flg': section_model.apparence_flg,
        }
        return Response(obj)


class SectionDataUpdate(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        section_model = SectionModel.objects.get(id=request.data["id"])
        section_model.appearance_date = request.data["appearance_date"]
        section_model.start_time = request.data["start_time"]
        section_model.allotted_time = request.data["allotted_time"]
        section_model.artist_name = request.data["artist_name"]
        section_model.other1 = request.data["other1"]
        section_model.other2 = request.data["other2"]
        section_model.other3 = request.data["other3"]
        section_model.other4 = request.data["other4"]
        section_model.other5 = request.data["other5"]
        section_model.official_url = request.data["official_url"]
        section_model.twitter_id = request.data["twitter_id"]
        section_model.insta_id = request.data["insta_id"]
        section_model.stage_id = request.data["stage_id"]
        section_model.save()
        # POSTリクエストで送信されたデータを取得する
        return Response({
                "error": "",
                "success": "更新が完了しました。",
            }, status=200)

router = routers.DefaultRouter()
# router.register(r'sections', SectionViewSet)
# router.register(r'test', TestSet)
# router.register(r'api', HelloView)
class AllModelReturn(ListCreateAPIView):    
   def post(self, request, *args, **kwargs):
        all_fes_model = FesModel.objects.all()
        all_stage_model = StageModel.objects.all()
        all_section_model = SectionModel.objects.all().order_by('-id')[:50]
       
        fes_serializer = FesModelSerializer(all_fes_model, many=True)
        stage_serializer = StageModelSerializer(all_stage_model, many=True)
        section_serializer = SectionModelSerializer(all_section_model, many=True)
        
        return Response({
            "error": "",
            "success": "更新が完了しました。",
            "fes":fes_serializer.data,
            "stage":stage_serializer.data,
            "section":section_serializer.data,
            }, status=200)

class OperateDbFesCreate(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        fes_model = FesModel()
        fes_model.name = request.data["name"]
        fes_model.year = request.data["year"]
        fes_model.event_date = request.data["eventDate"]
        fes_model.save()
        # POSTリクエストで送信されたデータを取得する
        return Response({
            "error": "",
            "success": "更新が完了しました。",
            "data":f"{fes_model.id}:{fes_model.name}",
            }, status=200)
    
class OperateDbStageCreate(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        stage_model = StageModel()
        stage_model.stage_id = request.data["stageId"]
        stage_model.name = request.data["stageName"]
        stage_model.place = request.data["color"]
        stage_model.color = request.data["color"]
        # 外部キーなので注意
        stage_model.fes_id_id = request.data["fesIdId"]
        stage_model.stage_image_path1 = request.data["stageImagePath1"]
        stage_model.save()
        # POSTリクエストで送信されたデータを取得する
        return Response({
            "error": "",
            "success": "更新が完了しました。",
            "data":f"{stage_model.id}:{stage_model.name}",
            }, status=200)
    
class OperateDbSectionCreate(ListCreateAPIView):
  def post(self, request, *args, **kwargs):

        # start_timeをイギリス時間ではなく、日本の時間に合わせる
        tz = timezone.get_current_timezone()
        target_time = f'1899-12-30 {request.data["start_time"]}:00'
        format_string = "%Y-%m-%d %H:%M:%S"
        datetime_object = datetime.strptime(target_time, format_string)
        tokyo_datetime = datetime_object+timedelta(hours=9)

        section_model = SectionModel()
        section_model.appearance_date = request.data["appearance_date"]
        section_model.start_time = tokyo_datetime
        section_model.allotted_time = request.data["allotted_time"]
        section_model.artist_name = request.data["artist_name"]
        section_model.other1 = request.data["other1"]
        section_model.other2 = request.data["other2"]
        section_model.other3 = request.data["other3"]
        section_model.other4 = request.data["other4"]
        section_model.other5 = request.data["other5"]
        section_model.official_url = request.data["official_url"]
        section_model.twitter_id = request.data["twitter_id"]
        section_model.insta_id = request.data["insta_id"]
        section_model.apparence_flg = True

        section_model.fes_id_id = request.data["fes_id"]
        section_model.live_category_id = 1
        section_model.stage_id = request.data["stage_id"]
        section_model.save()

        # POSTリクエストで送信されたデータを取得する
        return Response({
                "error": "",
                "success": "更新が完了しました。",
                "data":f"{section_model.id}:{section_model.artist_name}",
            }, status=200)
  
class DeleteFesModel(ListCreateAPIView):
  def post(self, request, *args, **kwargs):
      try:
        target_id = request.data["id"]
        record = FesModel.objects.get(id=target_id)
        record.delete()
        return Response({
          "error": "",
          "success": "削除しました",
          }, status=200)  # 削除成功
      except:
          return Response({
              "error": "システムエラーが発生しました",
              "success": "",
          }, status=200)

class DeleteStageModel(ListCreateAPIView):
  def post(self, request, *args, **kwargs):
      try:
        target_id = request.data["id"]
        record = StageModel.objects.get(id=target_id)
        record.delete()
        return Response({
          "error": "",
          "success": "削除しました",
          }, status=200)  # 削除成功
      except:
          return Response({
              "error": "システムエラーが発生しました",
              "success": "",
          }, status=200)
      
class DeleteSectionModel(ListCreateAPIView):
  def post(self, request, *args, **kwargs):
      try:
        target_id = request.data["id"]
        record = SectionModel.objects.get(id=target_id)
        record.delete()
        return Response({
          "error": "",
          "success": "削除しました",
          }, status=200)  # 削除成功
      except:
          return Response({
              "error": "システムエラーが発生しました",
              "success": "",
          }, status=200)