# Generated by Django 2.1.7 on 2019-05-25 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodcutSearch', '0012_auto_20190526_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
