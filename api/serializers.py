from rest_framework import serializers
from .models import FesModel, StageModel,CategoryModel,SectionModel,UserModel,MySectionModel,MyTiteModel

class FesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FesModel
        fields = '__all__'

class StageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageModel
        fields = '__all__'

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel

class SectionModelSerializer(serializers.ModelSerializer):
    class Meta:
      model = SectionModel
      fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

class MySectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySectionModel
        fields = '__all__'

class MyTiteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTiteModel
        fields = '__all__'

#-  0621 GPT -----------------------------

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageModel
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionModel
        fields = '__all__'