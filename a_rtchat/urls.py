from django.urls import path, include
from .views import *

urlpatterns = [
    path('', chat_view, name='home'),
    path('chat/<user_name>/', get_object_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>/send/', chat_view, name='chatroom'),

]