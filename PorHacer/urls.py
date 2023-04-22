# todo/todo/urls.py : Main urls.py
from django.contrib import admin
from django.urls import path,re_path, include
from api import urls as tareas_urls
from app import urls as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(tareas_urls)),
    re_path(r'^', include(app_urls)),
]