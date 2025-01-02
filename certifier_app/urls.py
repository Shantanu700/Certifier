from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("login/", views.signin),
    path("logout/", views.signout),
    path("generate-certificate/", views.generate_certificate),
    path("download_zip/", views.test),
    path("test2/", views.test2),
]