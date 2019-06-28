from django.db import models


class NewPhone(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='New_Phone', default="")
    text = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.name} NewPhone'


class TopRated(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Top_Rated')
    price = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.name} TopRated'


class Popular(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Popular_phone')
    price = models.CharField(max_length=8, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} Popular'


class Flagship(models.Model):
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    image = models.ImageField(upload_to='flagship_phone')
    price = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.brand} Flagship'


class SmartPhoneComparison(models.Model):
    name1 = models.CharField(max_length=50)
    image1 = models.ImageField(upload_to='phone_comparison')
    name2 = models.CharField(max_length=50)
    image2 = models.ImageField(upload_to='phone_comparison')

    def __str__(self):
        return f"{self.name1 +' vs ' + self.name2} SmartPhoneComparison"
