from ..models import SectionModel,StageModel,MySectionModel
from rest_framework.response import Response
import datetime


class MyTiteGenerator:
    @classmethod
    def get(self, obj ,request):
        param_value = request.query_params.get('id')
        # idパラメータを使ってモデルオブジェクトをフィルタリングして取得
        queryset = SectionModel.objects.filter(fes_id=param_value)
        serializer = obj.serializer_class(queryset, many=True)
        return serializer.data

    @classmethod
    def post(self, obj, request):
        # POSTリクエストで送信されたデータを取得する
        data = request.data
        # POSTで送られてきたidに紐づくSectionを返す。
        queryset = SectionModel.objects.filter(id__in=data["id"])
        if len(queryset) == 0:
          result = {
            'myTiteSections': [],
            'errorMsg': '1つ以上選んで下さい。'
          }
          return {"message": result}
        # 対象hの日付
        # date = queryset[0].appearance_date
        
        stage_model = StageModel.objects.filter(fes_id_id=request.data["fes_id"])
        # 後々別パラメーターでリストで取得
        my_section_model = MySectionModel.objects.filter(
            # id__in=data["my_sec_id"]
            fes_id_id=request.data["fes_id"],
            # date=date,
            user_id=request.data["user_id"]
            )
        
        my_section_list = []
        for my_section in my_section_model:
            my_section_list.append(my_section.id)

        print("■■■■■■■■■■■■■■■■■■■")
        print(my_section_list)


        
        stage_dict = {}
        for stage in stage_model:
          stage_dict[stage.id] = stage.stage_image_path1

        res_list = []
        time_list = []
        # 選択したセクション
        for query in queryset:
            obj={
              'id':query.id,
              'fes_id':query.fes_id.id,
              'appearance_date':query.appearance_date,
              # stage_idを仮指定
              'stage':0,
              'start_time':query.start_time,
              'allotted_time':query.allotted_time,
              'live_category':query.live_category.id,
              'artist_name':query.artist_name,
              # 'apparence_flg':query.apparence_flg,
              # 'change_time_flg':query.change_time_flg,
              'other1':query.other1,
              # 'other2':query.other2,
              # 'official_url':query.official_url,
              # 'twitter_id':query.twitter_id,
              # 'insta_id':query.insta_id,
              'org_stage_id':query.stage.id
              }
            time_list.append(query.start_time)
            # 選択してきたSectionをリストに格納
            res_list.append(obj)

        # マイセクション
        for query in my_section_model:
            obj={
              'id':query.id,
              'fes_id':query.fes_id.id,
              'stage':0,
              'start_time':query.start_time,
              'allotted_time':query.allotted_time,
              'live_category':1,
              'artist_name':query.title,
              'other1':query.other1,
              }
            time_list.append(query.start_time)
            # 選択してきたSectionをリストに格納
            res_list.append(obj)

        # 各Sectionのstart_timeを時間順にソート
        time_list.sort()

        continue_flag = True
        start_time = time_list[0]
        end_time = time_list[len(time_list)-1]
        target_time = start_time
        stage_id = 0
        return_list = []
        error_msg = ""

        try:
          # 自分でもよくわからないアルゴリズム、、
          while continue_flag:
              for i,res in enumerate(res_list):
                  # target_timeと同じresのデータを探す
                  if res['start_time'] == target_time:
                      copy_sec = res
                      res_list.pop(i)
                      copy_sec['stage'] = stage_id
                      if 'org_stage_id' in res:
                        copy_sec['stage_img_url'] = stage_dict[res['org_stage_id']]
                      return_list.append(copy_sec)

                      # 一致したtimeをtime_listから取り除く
                      for j ,time in enumerate(time_list):
                          if time == target_time:
                              time_list.pop(j)
                              break
                      # 後ほど5足すので5引いておく、的な？
                      target_time = target_time + datetime.timedelta(minutes=copy_sec['allotted_time']-5)
                      continue
              if len(time_list) == 0:
                  continue_flag = False
                  # ループ終了
                  break

              if target_time <= end_time:
                  # 5分繰り上げて再ループ
                  target_time = target_time + datetime.timedelta(minutes=5)
                  continue
              else:
                  stage_id = stage_id + 1
                  if stage_id==4:
                      # インデックスオーバー強制終了
                      result = {
                          'myTiteSections': [],
                          'errorMsg': "並行して表示できる数を超えています。"
                      }
                      return {"message": result}

                  target_time = start_time
                  continue
        except Exception as e:
            print("■■■ ERROR ■■■")
            print(e)
            error_msg = "システムエラーが発生しました。"
            # エラーを通知してほしい...

        result = {
            'myTiteSections': return_list,
            'errorMsg': error_msg,
            'orgSectionList':data["id"],
            'orgMySectionList':my_section_list
        }

        return {"message": result}

