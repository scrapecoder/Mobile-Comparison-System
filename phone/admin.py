from django.contrib import admin
from .models import NewPhone, TopRated, Popular, Flagship, SmartPhoneComparison

admin.site.register(NewPhone)
admin.site.register(TopRated)
admin.site.register(Popular)
admin.site.register(Flagship)
admin.site.register(SmartPhoneComparison)