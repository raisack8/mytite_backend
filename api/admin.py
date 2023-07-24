from django.contrib import admin
from .models import (
    FesModel,
    StageModel,
    CategoryModel,
    SectionModel,
    UserModel,

)

# Register your models here.
admin.site.register(FesModel)
admin.site.register(StageModel)
admin.site.register(CategoryModel)
admin.site.register(SectionModel)
admin.site.register(UserModel)