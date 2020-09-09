from django.shortcuts import render, redirect
from . import models
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt
from datetime import datetime


def checklogin(request):
    errors = {}
    if "email" not in request.session:
        errors['email'] = "<div class='ohno'>Please log in</div>"
        return False
    return True


def index(request):
    if request.method == "GET":
        if "email" in request.session:
            return render(request, "wall.html")
        else:
            return render(request, "index.html")
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            request.session['last_name'] = request.POST['last_name']
            request.session['first_name'] = request.POST['first_name']
            request.session['email'] = request.POST['email']
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            hash = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                           email=request.POST['email'], birthdate=datetime.strptime(request.POST['birthdate'], '%Y-%m-%d'), password=hash)
            request.session['email'] = request.POST['email']
            user = User.objects.get(email=request.POST['email'])
            request.session['first_name'] = user.first_name
        return redirect("/wall")


def wall(request):
    if not checklogin(request):
        return redirect('/')
    context = {
        "user_info": User.objects.get(email=request.session['email']),
        "all_messages": Message.objects.all().order_by("-created_at"),
        "all_comments": Comment.objects.all().order_by("-created_at")
    }
    return render(request, "wall.html", context)


def postmessage(request):
    if request.method == "POST":
        new_message = Message.objects.create(
            message=request.POST['message'], user=User.objects.get(id=request.POST['user_id']))
        return redirect("/wall")


def postcomment(request):
    if request.method == "POST":
        new_comment = Comment.objects.create(comment=request.POST['comment'], message=Message.objects.get(
            id=request.POST['message_id']), user=User.objects.get(id=request.POST['user_id']))
        return redirect("/wall")


def logout(request):
    if "email" in request.session:
        del request.session["email"]
    if "first_name" in request.session:
        del request.session["first_name"]
    if "last_name" in request.session:
        del request.session["last_name"]
    return redirect("/")


def delete(request, id):
    Message.objects.get(id=id).delete()
    return redirect ("/wall")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        request.session['email'] = request.POST['email']
        user = User.objects.get(email=request.POST['email'])
        print(user)
        request.session['first_name'] = user.first_name
        return redirect("/wall")
