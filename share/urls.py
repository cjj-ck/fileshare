from django.urls import path
from .views import Index, FileManage, DisplayFiles, SearchFile

app_name = 'share'

urlpatterns = [
    path('', Index, name='index'),
    path('s/<code>', DisplayFiles, name='display'),
    path('manage/', FileManage, name='manage'),
    path('search/', SearchFile, name='search'),
]