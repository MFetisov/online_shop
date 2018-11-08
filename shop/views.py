import os
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib import auth
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from shop import settings
from shop.form import *
from shop.models import *


def index(request):
    user = auth.get_user(request)

    products_Images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_phones = products_Images.filter(product__category__id=1)
    products_images_laptops = products_Images.filter(product__category__id=2)

    if user.is_anonymous:
        return render(request, 'shop//index/index.html')
    else:
        return render(request, 'shop/index/index.html', locals())


def login(request):
    args = {}
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден!"
            return render(request, 'shop/login.html', args)
    else:
        return render(request, 'shop/login.html', args)


def register(request):
    args = {'form': UserSignUpForm}
    if request.POST:
        newuser_form = UserSignUpForm(request.POST)
        if request.POST['password'] != request.POST['password_confirmation']:
            return redirect('/register/')
        elif newuser_form.is_valid():
            newuser = User.objects.create(username=request.POST['username'],
                                          email=request.POST['email'],
                                          # first_name=request.POST['first_name'],
                                          # last_name=request.POST['last_name'],
                                          # phoneNumber=request.POST['phoneNumber'],
                                          )
            newuser.set_password(request.POST['password_confirmation'])
            newuser.save()
            username = request.POST.get("username", '')
            password = request.POST.get("password", '')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render(request, 'shop/register.html', args)



def logout(request):
    auth.logout(request)
    return redirect('/')



