from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
from .models import User, Service, AboutUs, DoctorCard, Mention, News, Appointment

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

        return render(request, 'contact.html', {'message_name':message_name})

    else:
        return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})

def service(request):
    service = Service.objects.all()

    return render(request, 'service.html', {'service':service})

def pricing(request):
    return render(request, 'pricing.html', {})


def appointment(request):
    print(request.POST)
    if request.method == "POST":
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_message = request.POST['your-message']
        your_time = datetime.strptime(request.POST['your-time'], '%H:%M')
        your_date = datetime.strptime(request.POST['your-date'], '%Y-%m-%d')


        ### Send an Email Start ###
        new_appointment = Appointment.objects.create(
            date=your_date,
            time=your_time,
            service=Service.objects.latest('id'),
            client=User.objects.latest('id'),
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

        return render(request, 'appointment.html', {
            'your_name':your_name,
            'your_phone':your_phone,
            'your_email':your_email,
            'your_address':your_address,
            'your_schedule': None,
            'your_date': None,
            'your_message': your_message
        })

    else:
        return render(request, 'home.html', {})


def booknow(request):
    return render(request, 'booknow.html')


def single_news(request, id):
    return HttpResponse(1)
