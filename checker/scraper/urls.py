from django.urls import path
from . import views

app_name = "scraper"

urlpatterns = [
    path('', views.index, name = "index"),
    path('subscribe', views.subscribe, name ="subscribe"),
    path('unsubscribe', views.unsubscribe, name="unsubscribe"),
    path('export', views.request_data_export, name="export"),    
]