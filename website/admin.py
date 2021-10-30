from django.contrib import admin

from .models import (Service, Appointment, Contact,
                     DoctorCard, AboutUs, Mention,
                     News, Bar)


class BarInline(admin.TabularInline):
    model = Bar
    extra = 0

class AboutUsAdmin(admin.ModelAdmin):
    inlines = [BarInline]


admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Contact)
admin.site.register(DoctorCard)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Mention)
admin.site.register(News)
