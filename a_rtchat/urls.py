from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('profiles/', chat_view, name='profiles'),
    path('chat/<user_name>/', get_object_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>/send/', chat_view, name='chatroom'),
    path('reviews/', reviews, name='reviews'),

]