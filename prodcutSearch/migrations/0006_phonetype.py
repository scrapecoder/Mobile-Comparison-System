# Generated by Django 2.1.7 on 2019-04-07 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodcutSearch', '0005_post_smallcontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='phone_type')),
            ],
        ),
    ]
