# Generated by Django 4.2.2 on 2023-07-24 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stagemodel',
            name='stage_image_path1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='stagemodel',
            name='stage_image_path2',
            field=models.TextField(null=True),
        ),
    ]
