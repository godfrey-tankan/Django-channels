from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import Http404
from .content_processor import custom_context
from django.db.models import Q
from a_users.models import Profile
import json

# Create your views here.
@login_required
def chat_view(request,chatroom_name='public-chat'):
    request_user_interests = get_object_or_404(Profile, user=request.user).interests.split(',')[0]
    if len(chatroom_name) > 20:
        chatroom_name = chatroom_name
    else:
        if request_user_interests.lower() == 'nostrings':
            chatroom_name = 'NoStrings'
        elif request_user_interests.lower() == 'love':
            chatroom_name = 'Love_Birds'
        elif request_user_interests.lower() == 'friendship':
            chatroom_name = 'Real-Friends'
        elif request_user_interests.lower() == 'hookups':
            chatroom_name = 'Hookups'
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:20]
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = chat_group 
            message.author = request.user
            message.save()
            context = {'message':message, 'user':request.user}
            return render(request, 'a_rtchat/partials/chat_message_p.html',context)
    try:
        request_user_profile = Profile.objects.get(user=request.user)
        request_user_interests = request_user_profile.interests.split(',')
        q_objects = [Q(interests__icontains=interest.strip()) for interest in request_user_interests]
        combined_q = q_objects[0]
        for q in q_objects[1:]:
            combined_q |= q
        all_users = Profile.objects.filter(combined_q).exclude(user=request.user)
    except:
        all_users = None
        
    context = {'chat_messages':chat_messages, 'form':form, 'chatroom_name':chatroom_name, 'other_user':other_user, 'all_users':all_users}
    return render(request, 'a_rtchat/chat.html', context)

def home(request):
    context =custom_context(request)
    reviews = Reviews.objects.all()[:10]
    context['reviews']= reviews
    return render(request, 'index.html', context)

@login_required
def get_object_or_create_chatroom(request,user_name):

    if request.user.username == user_name:
        return redirect('home')


    other_user = User.objects.get(username=user_name)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom =chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(request.user,other_user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user,other_user)

    return redirect('chatroom',chatroom.group_name)

def review_detail(request,review_id):
    review = get_object_or_404(Reviews, id=review_id)
    reviews = Reviews.objects.all()
    context = {'review':review, 'reviews':reviews}
    return render(request, 'review_detail.html', context)


def reviews(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reviews = Reviews.objects.create(
                name = data['name'],
                phone = data['phone'],
                email = data['email'],
                review = data['comments']
            )
        except:
            ...
        
    try:
        reviews = Reviews.objects.all()[:10]
    except:
        reviews =None
    context ={
        'reviews':reviews
    }
   
    return render(request, 'index.html', context)