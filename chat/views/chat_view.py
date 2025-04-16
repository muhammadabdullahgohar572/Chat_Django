from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import UserRelation, Messages
from django.http.response import JsonResponse
from django.contrib import messages as django_messages


@login_required(login_url="login")
def chat(request, username):
    try:
        usersen = request.user
        friend = User.objects.get(username=username)
        exists = UserRelation.objects.filter(
            user=request.user, friend=friend, accepted=True
        ).exists()

        if not exists:
            django_messages.error(request, "You are not able to chat with this user.")
            return redirect("home")

    except User.DoesNotExist:
        return redirect("home")

    # Get the messages
    messages = Messages.objects.filter(
        sender_name=usersen, receiver_name=friend
    ) | Messages.objects.filter(sender_name=friend, receiver_name=usersen)

    if request.method == "POST":
        message_text = request.POST.get("message")
        image = request.FILES.get("image")
        
        if message_text or image:
            message = Messages.objects.create(
                sender_name=usersen,
                receiver_name=friend,
                description=message_text,
            )
            if image:
                message.photo = image
                message.save()
            return JsonResponse({"status": "success"})

    try:
        relation = UserRelation.objects.get(
            user=request.user, friend=friend, accepted=True
        )
        return render(
            request,
            "chat.html",
            {
                "relation_key": relation.relation_key,
                "messages": messages,
                "curr_user": usersen,
                "friend": friend,
            },
        )
    except UserRelation.DoesNotExist:
        django_messages.error(request, "Relation not found.")
        return redirect("home")
