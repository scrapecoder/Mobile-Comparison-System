# Generated by Django 2.1.7 on 2019-05-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodcutSearch', '0009_auto_20190526_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]