# Generated by Django 2.1.7 on 2019-04-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Popular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='Popular_phone')),
                ('price', models.CharField(max_length=8, null=True)),
            ],
        ),
    ]
