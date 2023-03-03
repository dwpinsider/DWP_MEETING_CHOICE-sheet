from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_meeting_register, name='vendor_meeting_register'),
]
