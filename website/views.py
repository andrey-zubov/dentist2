from django.shortcuts import render, HttpResponse, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .models import (User, Client, Service, AboutUs,
                     DoctorCard, Mention, News,
                     Appointment, Administrator, DoctorQuestion)

from datetime import datetime


def home(request):
    about_us = AboutUs.objects.all()
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
    about_us = AboutUs.objects.all()
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
    return render(request, 'auth.html', {'about_us': about_us})


def logout_view(request):
    logout(request)
    return redirect('home')


def registration(request):
    about_us = AboutUs.objects.all()

    err = None
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            if User.objects.filter(
                    Q(username=request.POST['username']) |
                    Q(email=request.POST['email'])).exists():
                err = 'Такой пользователь или телефон/email уже зарегистрированы'
                return render(request, 'registration.html', {'err': err,
                                                             'about_us': about_us,})

            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )
            new_client = Client.objects.create(
                address=request.POST['address'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                patronymic=request.POST['patronymic'],
                user=new_user,
                email=request.POST['email'],
                phone=request.POST['phone']
            )
            login(request, new_user)
            return redirect('home')

        err = 'Пароли должны совпадать'
    return render(request, 'registration.html', {'err': err,
                                                 'about_us': about_us,})


def contact(request):
    about_us = AboutUs.objects.all()

    if request.method == "POST":
        if 'message-name' in request.POST:
            message_name = request.POST['message-name']
            message_email = request.POST['message-email']
        else:
            message_name = request.user.first_name
            message_email = request.user.email
        message = request.POST['message']

        new_mention = Mention.objects.create(content=message,
                                             name=message_name)
        new_mention.save()

    return render(request, 'contact.html', {'about_us': about_us})


def about(request):
    about_us = AboutUs.objects.all()

    doctors = DoctorCard.objects.all()
    mentions = Mention.objects.all().reverse()[:3]
    return render(request, 'about.html', {'about_us': about_us,
                                          'doctors': doctors,
                                          'mentions': mentions})


def service(request):
    about_us = AboutUs.objects.all()

    services = Service.objects.all()
    mentions = Mention.objects.all().reverse()[:3]
    news = News.objects.all().reverse()[:3]
    return render(request, 'service.html', {'service': services,
                                            'mentions': mentions,
                                            'news': news,
                                            'about_us': about_us,})


def pricing(request):
    about_us = AboutUs.objects.all()

    services = Service.objects.all()
    return render(request, 'pricing.html', {'services': services,
                                            'about_us': about_us,})


def appointment(request):
    about_us = AboutUs.objects.all()

    if request.method == "POST":
        message = request.POST['message']
        time = datetime.strptime(request.POST['time'], '%H:%M')
        date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
        serv = Service.objects.get(id=request.POST['service'])
        doctor = DoctorCard.objects.get(id=request.POST['doctor'])
        client = Client.objects.get(user_id=request.user.id)

        new_appointment = Appointment.objects.create(
            date=date,
            time=time,
            service=serv,
            client=client,
            client_comment=message,
            doctor=doctor,
            clinic_id=request.POST['clinic']
        )
        new_appointment.save()
        # send_mail(
        #     'Appointment Request', # subject
        #     appointment, # message
        #     your_email, # from email
        #     ['iii2468@gmail.com'], # To email
        #     # ['aaaaa@gmail.com','bbbb@gmail.com'], # To email
        # )
        ### Send an Email End ###

        return render(request, 'appointment.html', {'your_name': client.first_name,
                                                    'your_message': message,
                                                    'your_phone': client.phone,
                                                    'your_email': client.email,
                                                    'your_time': time,
                                                    'your_date': date,
                                                    'about_us': about_us})

    else:
        return render(request, 'home.html', {'about_us': about_us,})


def booknow(request):
    about_us = AboutUs.objects.all()

    serv = Service.objects.all()
    doctors = DoctorCard.objects.all()
    return render(request, 'booknow.html', {'services': serv,
                                            'doctors': doctors,
                                            'about_us': about_us,})


def single_news(request, id):
    about_us = AboutUs.objects.all()

    news = News.objects.get(id=id)
    return render(request, 'news.html', {'news': news,
                                         'about_us': about_us})


def ask_doctor(request, doc_id):
    doctor = DoctorCard.objects.get(id=doc_id)
    if request.method == 'POST':
        DoctorQuestion.objects.create(
            client=Client.objects.get(user_id=request.user.id),
            doctor=doctor,
            text=request.POST['question']
        )
        return redirect('home')

    return render(request, 'ask_doctor.html', {'doctor': doctor})


def cabinet(request, user_id):
    about_us = AboutUs.objects.all()

    if Client.objects.filter(user_id=user_id).exists():
        client = Client.objects.get(user_id=user_id)
        questions = DoctorQuestion.objects.filter(client=client).order_by('id').reverse()[:5]
        if request.method == 'POST':
            client.first_name = request.POST['name']
            client.last_name = request.POST['surname']
            client.patronymic = request.POST['patronymic']
            client.email = request.POST['email']
            client.phone = request.POST['tel']
            client.address = request.POST['address']
            client.save()

        user_appointment = Appointment.objects.filter(client=client)
        return render(request, 'cabinet.html', {'client': client,
                                                'user_appointment': user_appointment,
                                                'about_us': about_us,
                                                'questions': questions})

    elif DoctorCard.objects.filter(user_id=user_id).exists():
        doctor = DoctorCard.objects.get(user_id=user_id)
        quesions = DoctorQuestion.objects.filter(doctor=doctor).filter(is_answered=False)
        if request.method == 'POST':
            doctor.first_name = request.POST['name']
            doctor.last_name = request.POST['surname']
            doctor.patronymic = request.POST['patronymic']
            doctor.email = request.POST['email']
            doctor.phone = request.POST['tel']
            doctor.specialization = request.POST['specialization']
            doctor.description = request.POST['description']
            doctor.save()

        user_appointment = Appointment.objects.filter(doctor=doctor)
        return render(request, 'doctor_cabinet.html', {'doctor': doctor,
                                                       'user_appointment': user_appointment,
                                                       'about_us': about_us,
                                                       'questions': quesions})

    elif Administrator.objects.filter(user_id=user_id).exists():
        administrator = Administrator.objects.get(user_id=user_id)
        clients = Client.objects.all()

        return render(request, 'administrator_cabinet.html', {'about_us': about_us,
                                                              'administrator': administrator,
                                                              'clients': clients})


def ajax_save_question(request):
    question = DoctorQuestion.objects.get(id=request.POST['question_id'])
    question.answer = request.POST['answer']
    question.save()
    return HttpResponse(1)


def ajax_save_client(request):
    client = Client.objects.get(id=request.POST['client_id'])
    client.first_name = request.POST['first_name']
    client.last_name = request.POST['last_name']
    client.patronymic = request.POST['patronymic']
    client.email = request.POST['email']
    client.phone = request.POST['phone']
    client.address = request.POST['address']
    client.save()
    return HttpResponse(1)


def ajax_delete_client(request):
    Client.objects.get(id=request.POST['client_id']).delete()
    return HttpResponse(1)


def doctor_appointment_report(request, a_id):
    appointment = Appointment.objects.get(id=a_id)
    if request.method == 'POST':
        appointment.report = request.POST['appointment_report']
        appointment.save()
        return redirect('cabinet_page', request.user.id)
    return render(request, 'reports/doc_appointment.html', {'appointment': appointment})


def user_chat(request, room_name):
    return render(request, 'chat/chat_room.html', {'room_name': room_name})


def administrator_chat(request, room_name):
    return render(request, 'chat/chat_administrator.html', {'room_name': room_name})

