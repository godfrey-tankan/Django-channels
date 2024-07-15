from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import Http404

# Create your views here.
@login_required
def chat_view(request,chatroom_name='public-chat'):
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
        
    context = {'chat_messages':chat_messages, 'form':form, 'chatroom_name':chatroom_name, 'other_user':other_user}
    return render(request, 'a_rtchat/chat.html', context)

def home(request):
    profile = get_object_or_404(User, id=request.user.id)

    context = {'name':profile.username}
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
    