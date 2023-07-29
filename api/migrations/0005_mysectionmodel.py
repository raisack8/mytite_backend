# Generated by Django 4.2.2 on 2023-07-29 11:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_mytitemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySectionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(default=datetime.datetime.now)),
                ('date', models.DateField()),
                ('start_time', models.DateTimeField()),
                ('allotted_time', models.IntegerField()),
                ('title', models.TextField()),
                ('other1', models.TextField(null=True)),
                ('other2', models.TextField(null=True)),
                ('fes_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fesmodel')),
            ],
        ),
    ]
