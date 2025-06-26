# Django
from django.urls import path
# Views
from .views import PhotoListView

app_name = 'web_motorcycle_photo' 

urlpatterns = [
    path('motorcycle-photo/list', PhotoListView.as_view(), name='list'),
]