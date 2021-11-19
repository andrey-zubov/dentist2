from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .import views
from .api.api import MessageModelViewSet, UserModelViewSet, ClientUserModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')
router.register(r'administrators', ClientUserModelViewSet, basename='administartor-api')


urlpatterns = [
    path('', views.home, name="home"),
    path(r'api/v1/', include(router.urls)),

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
    path('single_news/<int:id>', views.single_news, name='single_news_page'),


    path('chat/<str:room_name>/', views.user_chat, name='user_chat_page'),
    path('admin-chat/<str:room_name>/', views.administrator_chat, name='admin_chat_page')

]
