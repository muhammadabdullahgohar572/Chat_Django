from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import UserRelation, Messages
from django.http.response import JsonResponse
from django.contrib import messages as django_messages
from django.conf import settings
import cloudinary.uploader
from datetime import datetime

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
        message_text = request.POST.get("message", "").strip()
        images = request.FILES.getlist('images')  # Get all uploaded images
        
        response_data = {"status": "success", "image_urls": []}
        messages_created = []
        
        # Create message only if there's content or images
        if message_text or images:
            # Handle text message if exists
            if message_text:
                message = Messages.objects.create(
                    sender_name=usersen,
                    receiver_name=friend,
                    description=message_text,
                )
                messages_created.append(message.id)
                response_data['message_id'] = message.id
            
            # Handle image uploads using Cloudinary
            for image in images:
                if image:  # Check if file exists
                    # Upload image to Cloudinary
                    upload_result = cloudinary.uploader.upload(
                        image,
                        folder="chat_images/"
                    )
                    
                    # Create a new message for the image
                    message = Messages.objects.create(
                        sender_name=usersen,
                        receiver_name=friend,
                        photo=upload_result['secure_url']  # Store Cloudinary URL
                    )
                    messages_created.append(message.id)
                    response_data['image_urls'].append(message.photo)
            
            response_data['messages_created'] = messages_created
            return JsonResponse(response_data)
        else:
            return JsonResponse({"status": "error", "message": "No content provided"}, status=400)

    try:
        relation = UserRelation.objects.get(
            user=request.user, friend=friend, accepted=True
        )
        return render(
            request,
            "chat.html",
            {
                "relation_key": relation.relation_key,
                "messages": messages.order_by('timestamp'),
                "curr_user": usersen,
                "friend": friend,
            },
        )
    except UserRelation.DoesNotExist:
        django_messages.error(request, "Relation not found.")
        return redirect("home")