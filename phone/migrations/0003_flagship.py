# Generated by Django 2.1.7 on 2019-04-17 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0002_popular'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flagship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='flagship_phone')),
                ('price', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]