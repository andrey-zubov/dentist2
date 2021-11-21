from django.contrib import admin

from .models import (Service, Appointment,
                     DoctorCard, AboutUs, Mention,
                     News, Client, Administrator,
                     MessageModel, DoctorQuestion)


admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(DoctorCard)
admin.site.register(AboutUs)
admin.site.register(Mention)
admin.site.register(News)
admin.site.register(Client)
admin.site.register(Administrator)
admin.site.register(MessageModel)
admin.site.register(DoctorQuestion)
