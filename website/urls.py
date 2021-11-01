from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('service/', views.service, name="service"),
    path('pricing/', views.pricing, name="pricing"),
    path('appointment/', views.appointment, name="appointment"),
    path('booknow/', views.booknow, name="booknow"),
    path('single_news/<int:id>', views.single_news, name='single_news_page'),
]
