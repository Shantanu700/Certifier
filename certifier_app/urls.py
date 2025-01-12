from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("login/", views.signin),
    path("logout/", views.signout),
    path("generate-certificate/", views.generate_certificate),
    path("download-zip/", views.test),
    path("file-manager/", views.manage_file_folders),
    path("file-manager/<str:task>/", views.manage_file_folders),
    path("file-manager/<str:task>/<str:object_type>/", views.manage_file_folders),
    path("test2/", views.test2),
]