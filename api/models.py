from django.db import models
import datetime

# Create your models here.


class FesModel(models.Model):
  name = models.TextField()
  year = models.DateField()
  event_date = models.DateField()
  place = models.TextField(null=True)
  official_url = models.TextField(null=True)
  twitter_id =  models.TextField(null=True)
  insta_id =  models.TextField(null=True)
  image_url1 =  models.TextField(null=True)
  image_url2 =  models.TextField(null=True)
  image_url3 =  models.TextField(null=True)
  other1 =  models.TextField(null=True)
  other2 =  models.TextField(null=True)
  
class StageModel(models.Model):
  fes_id = models.ForeignKey(FesModel, on_delete=models.CASCADE)
  stage_id = models.IntegerField()
  name = models.TextField()
  place = models.TextField()
  color = models.TextField(default="#C0C0C0")
  stage_image_path1 = models.TextField(null=True)
  stage_image_path2 = models.TextField(null=True)

class CategoryModel(models.Model):
  fes_id = models.ForeignKey(FesModel, on_delete=models.CASCADE)
  name =  models.TextField()
  other1 =  models.TextField(null=True)
  other2 =  models.TextField(null=True)

class SectionModel(models.Model):
  fes_id = models.ForeignKey(FesModel, on_delete=models.CASCADE) # 別途DB?
  appearance_date = models.DateField()
  stage = models.ForeignKey(StageModel, on_delete=models.CASCADE) # 別途DB?
  start_time = models.DateTimeField()
  # プルダウンとかから選択させるよう実装すればずれが生じなくなるか？
  allotted_time = models.IntegerField()
  live_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE) # 別途DB?
  artist_name = models.TextField()
  apparence_flg = models.BooleanField(default=True)
  change_time_flg = models.BooleanField(null=True)
  # other1 = セカンドタイトル
  other1 = models.TextField(null=True)
  # other2 = 画像URL(例：/resources/tif2023/Appare.jpg)
  other2 = models.TextField(null=True)
  other3 = models.TextField(null=True)
  other4 = models.TextField(null=True)
  other5 = models.TextField(null=True)
  official_url =  models.TextField(null=True)
  twitter_id =  models.TextField(null=True)
  insta_id =  models.TextField(null=True)
  def __str__(self):
    return self.artist_name

class UserModel(models.Model):
  registration_date = models.DateField(default=datetime.datetime.now)
  username = models.TextField()
  user_id = models.TextField()
  email = models.TextField(null=True)
  user_sns_id1 = models.TextField(null=True)
  user_sns_id2 = models.TextField(null=True)
  user_sns_id3 = models.TextField(null=True)
  password = models.TextField()
  gender = models.TextField(null=True)
  age = models.IntegerField(null=True)
  residence = models.TextField(null=True) # 住まい
  active_level = models.IntegerField(null=True)
  subscribe_level = models.IntegerField(null=True)
  invitation_flg = models.BooleanField(null=True)
  my_tite_list = models.TextField(null=True) # [1,2,5,6]のように配列で格納したい　配列→文字列変換
  follow_list = models.TextField(null=True) # [1,2,5,6]のように配列で格納したい　配列→文字列変換
  follower_list = models.TextField(null=True) # [1,2,5,6]のように配列で格納したい　配列→文字列変換

class MySectionModel(models.Model):
  create_date = models.DateField(default=datetime.datetime.now)
  '''fes_idが有れば日付を特定できる'''
  # date = models.DateField()
  start_time = models.DateTimeField()
  allotted_time = models.IntegerField()
  title = models.TextField()
  other1 = models.TextField(null=True)
  other2 = models.TextField(null=True)
  fes_id = models.ForeignKey(FesModel, on_delete=models.CASCADE) 
  user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE) # 別途DB?

class MyTiteModel(models.Model):
  create_date = models.DateField(default=datetime.datetime.now)
  section_list = models.TextField(null=True)
  my_section_list = models.TextField(null=True)
  user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE) # 別途DB?
  slot_num = models.IntegerField()
  title = models.TextField(null=True)
  explain = models.TextField(null=True)
  fes_id = models.ForeignKey(FesModel, on_delete=models.CASCADE) 
