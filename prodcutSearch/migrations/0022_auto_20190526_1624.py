# Generated by Django 2.1.7 on 2019-05-26 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prodcutSearch', '0021_auto_20190526_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='comment',
        ),
    ]
