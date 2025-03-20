from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verify_signature/<str:token>/', views.verify_signature, name='verify_signature'),
]