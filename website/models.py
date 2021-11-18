from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.shortcuts import reverse


class Administrator(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.user.is_staff = True
        self.user.user_permissions.set(Permission.objects.all().exclude(codename='delete_user'))
        self.user.save()
        super(Administrator, self).save(*args, **kwargs)

    def go_to_cabinet(self):
        return reverse('cabinet_page', kwargs={'id': self.user_id})


class Client(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=32,
                             verbose_name='Номер телефона',
                             unique=True)
    email = models.EmailField(verbose_name='Почта/email',
                              unique=True)
    address = models.TextField(null=True,
                               blank=True,
                               verbose_name='Физический адресс клиента')
    first_name = models.CharField(max_length=128,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=128,
                                 verbose_name='Фамилия')
    patronymic = models.CharField(max_length=128,
                                  verbose_name='Отчсество',
                                  null=True,
                                  blank=True)

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def go_to_cabinet(self):
        return reverse('cabinet_page', kwargs={'id': self.user_id})


class DoctorCard(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=32,
                             verbose_name='Номер телефона',
                             null=True,
                             blank=True)
    email = models.EmailField(verbose_name='Почта/email',
                              null=True,
                              blank=False)
    first_name = models.CharField(max_length=128,
                            verbose_name='Имя')
    last_name = models.CharField(max_length=128,
                               verbose_name='Фамилия')
    patronymic = models.CharField(max_length=128,
                                  verbose_name='Отчсество',
                                  null=True,
                                  blank=True)
    image = models.ImageField(upload_to='website/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    specialization = models.CharField(verbose_name='специалтзация',
                                      max_length=64)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def go_to_cabinet(self):
        return reverse('cabinet_page', kwargs={'id': self.user_id})

    class Meta:
        verbose_name = 'Карточка врача'
        verbose_name_plural = 'Карточки врачей'



class Service(models.Model):
    image = models.ImageField(upload_to='website/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')
    title = models.CharField(max_length=168, verbose_name='Название')
    content = models.TextField(verbose_name='Описание')
    price = models.DecimalField(decimal_places=2,
                                verbose_name='стоимость',
                                max_digits=16)


    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class Appointment(models.Model):
    register_date = models.DateTimeField(auto_now_add=True,
                                         editable=False,
                                         verbose_name='дата и время регистрации услуги')
    date = models.DateField(verbose_name="Дата приема")
    time = models.TimeField(verbose_name="Время приема")
    clinic = models.ForeignKey('AboutUs',
                               on_delete=models.CASCADE,
                               verbose_name='Клиника')
    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                verbose_name="Услугп")
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               verbose_name='Клиент')
    doctor = models.ForeignKey(DoctorCard,
                               on_delete=models.CASCADE,
                               verbose_name='Врач')
    client_comment = models.TextField(null=True,
                                      verbose_name='Комментарий клиента')

    class Meta:
        verbose_name = 'Визит к врачу'
        verbose_name_plural = 'Визиты к врачу'

    def __str__(self):
        return f'{self.id} {self.date} {self.time} {self.client}'


class AboutUs(models.Model):
    image = models.ImageField(upload_to='website/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')
    title = models.CharField(max_length=128, verbose_name='Название')
    content = models.TextField(verbose_name='Описание')
    address = models.CharField(max_length=256,
                               verbose_name='адрес')
    phone = models.CharField(max_length=32,
                             verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Почта/email',
                              unique=False,
                              blank=False)
    map_iframe = models.TextField(help_text="ссылка на встраивание карт")

    class Meta:
        verbose_name = 'клиника'
        verbose_name_plural = 'клиники'

    def __str__(self):
        return self.title


class Mention(models.Model):
    image = models.ImageField(upload_to='website/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')
    content = models.TextField(verbose_name='Описание')
    name = models.CharField(max_length=64, verbose_name="Имя")
    description = models.CharField(max_length=32,
                                   verbose_name='Описание клиента',
                                   null=True,
                                   blank=True,
                                   help_text='пример: "удаление зубов')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name}, {self.description}: {self.content[:24]}'


class News(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст новости')
    publish_date = models.DateField(editable=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_news_page', kwargs={'id': self.id})
