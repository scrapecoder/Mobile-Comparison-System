"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from phone import views as phone_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from phone.views import top_rated, top_popular, flagship_phone, smart_phone_comparison

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', include('prodcutSearch.urls')),

    path('Best Display/', phone_views.best_display, name='best_display_phone'),
    path('4g_phone/', phone_views.phone_4g, name='4g_phone'),
    path('gaming_phone.html/', phone_views.gaming_phone, name='gaming_phone'),
    path('greator_20k_phone/', phone_views.greator20, name='greator_20k_phone'),
    path('less_10k_phone/', phone_views.less10, name='less_10k_phone'),
    path('less_20k_phone/', phone_views.less20, name='less_20k_phone'),
    path(r'top_rated_scrape/', top_rated),
    path(r'popular_scrape/', top_popular),
    path(r'flagship_phone_scrape/', flagship_phone),
    path(r'smart_phone_comp_scrape/', smart_phone_comparison)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
