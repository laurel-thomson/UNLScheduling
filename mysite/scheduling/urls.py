from django.urls import path

from .views import scheduling

urlpatterns = [
    path('', scheduling.index, name='index')
]