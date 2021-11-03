from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .models import (User, Service, AboutUs,
                     DoctorCard, Mention, News,
                     Appointment, Contact)

from datetime import datetime


def home(request):
    about_us = AboutUs.objects.latest('id')
    doctors = DoctorCard.objects.all()
    services = Service.objects.all()
    mentions = Mention.objects.all().reverse()[:3]
    news = News.objects.all().reverse()[:3]
    return render(request, 'home.html', {'about_us': about_us,
                                         'doctors': doctors,
                                         'services': services,
                                         'mentions': mentions,
                                         'news': news})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            err = 'Введите верный пароль или зарегистрируйтесь'
            return render(request, 'auth.html', {'err': err})
    return render(request, 'auth.html', {})


def registration(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            if User.objects.filter(
                    Q(username=request.POST['username']) |
                    Q(phone=request.POST['phone']) |
                    Q(email=request.POST['email'])).exists():
                err = 'Такой пользователь или телефон/email уже зарегистрированы'
                return render(request, 'registration.html', {'err': err})

            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                address=request.POST['address'],
                phone=request.POST['phone'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                patronymic=request.POST['patronymic'],
                email=request.POST['email'],
            )
            new_user.save()

        err = 'Пароли должны совпадать'
    return render(request, 'registration.html', {})


def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']  # here message-name comes from contact.html file's input type name
        message_email = request.POST['message-email']
        message = request.POST['message']

        ### Send an Email Start ###
        send_mail(
            message_name, # subject
            message, # message
            message_email, # from email
            ['omarfaruk2468@gmail.com','mehedibinhafiz@gmail.com',], # To email
        )
        ### Send an Email End ###

        return render(request, 'contact.html', {'message_name': message_name})

    else:
        contact_info = Contact.objects.latest('id')
        return render(request, 'contact.html', {'contact_info': contact_info})


def about(request):
    about_us = AboutUs.objects.latest('id')
    doctors = DoctorCard.objects.all()
    mentions = Mention.objects.all().reverse()[:3]
    return render(request, 'about.html', {'about_us': about_us,
                                          'doctors': doctors,
                                          'mentions': mentions})


def service(request):
    services = Service.objects.all()
    mentions = Mention.objects.all().reverse()[:3]
    news = News.objects.all().reverse()[:3]
    return render(request, 'service.html', {'service': services,
                                            'mentions': mentions,
                                            'news': news})


def pricing(request):
    services = Service.objects.all()
    return render(request, 'pricing.html', {'services': services})


def appointment(request):
    print(request.POST)
    if request.method == "POST":
        message = request.POST['message']
        time = datetime.strptime(request.POST['time'], '%H:%M')
        date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
        serv = Service.objects.get(id=request.POST['service'])
        client = request.user

        new_appointment = Appointment.objects.create(
            date=date,
            time=time,
            service=serv,
            client=client,
            client_comment=message

        )
        new_appointment.save()
        # send_mail(
        #     'Appointment Request', # subject
        #     appointment, # message
        #     your_email, # from email
        #     ['omarfaruk2468@gmail.com'], # To email
        #     # ['omarfaruk2468@gmail.com','mehedibinhafiz@gmail.com'], # To email
        # )
        ### Send an Email End ###

        return render(request, 'appointment.html', {})

    else:
        return render(request, 'home.html', {})


def booknow(request):
    serv = Service.objects.all()
    return render(request, 'booknow.html', {'services': serv})


def single_news(request, id):
    news = News.objects.get(id=id)
    return render(request, 'news.html', {'news': news})
