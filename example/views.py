import random
from string import digits

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from djnotifier.utils import push_notification_to_user, push_notification_to_anonymous_users
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required


User = get_user_model()


def generate_random_username(size=3):
    return "user_" + "".join([random.choice(digits) for _ in range(size)])


def get_user_password():
    username = generate_random_username()
    password = 'password'
    try:
        user = User.objects.last()
        username = user.username
        user.set_password(password)
        user.save()
    except Exception as err:
        print(err)
        user = User(
            username=username,
            first_name=username.capitalize(),
            email=f"{username}@email.com"
        )
        user.set_password(password)
        user.save()
    return user, password


def authenticated_user_view(request):
    template = 'example/authenticated.html'
    context = {}
    user, password = get_user_password()
    print(user, password)
    is_auth = authenticate(username=user.username, password=password)
    print("is auth:", is_auth)
    if is_auth:
        login(request, user)
    return render(request, template, context)


def anonymous_users_view(request):
    template = 'example/anonymous.html'
    context = {}
    logout(request)
    return render(request, template, context)


def notify(request):
    template = 'example/notify.html'
    context = {
        "message": "Two notifications were sent. One was sent to all anonymous users and "
                   f"another one was sent to user with `pk={request.user.pk}`",
    }
    data1 = {
        "message": "Hello, guest. You just received a new offer!",
        "type": "success"
    }
    data2 = {
        "message": "Hello, root. You have 3 unread messages!",
        "type": "info"
    }
    push_notification_to_anonymous_users(data=data1)
    push_notification_to_user(data=data2, user=request.user)
    return render(request, template, context)
