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
    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration, name='registration_page'),
    path('cabinet/<int:user_id>', views.cabinet, name='cabinet_page'),
    path('single_news/<int:id>', views.single_news, name='single_news_page')
    ,
    path('test', views.chat_main, name='chat_main'),
    path('chat/<str:room_name>/', views.room, name='chat_room'),

]
