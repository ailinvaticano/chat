from django.urls import path
from .views import CreateChatBoxView, index, DetailChatBoxView, CreateMessageView, CreateUserView, logout_view
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', index, name='index'),
    path('create/', CreateChatBoxView.as_view(), name='chat_box_create'),
    path('detail/<int:pk>', DetailChatBoxView.as_view(), name='chat_box_detail'),
    path('detail/<int:pk>/createmessage/', CreateMessageView.as_view(), name='message_create'),
    path('createuser/', CreateUserView.as_view(), name='user_create'),
    path('logout/', logout_view,  name='logout'),
    path('login/', LoginView.as_view(), name='login'),
]
