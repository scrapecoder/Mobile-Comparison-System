# Generated by Django 2.1.7 on 2019-06-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0004_smartphonecomparison'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphonecomparison',
            name='image1',
            field=models.ImageField(upload_to='phone_comparison'),
        ),
        migrations.AlterField(
            model_name='smartphonecomparison',
            name='image2',
            field=models.ImageField(upload_to='phone_comparison'),
        ),
    ]
