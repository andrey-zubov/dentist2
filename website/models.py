from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):  # переопределение стандартной модели User
    POSITION_CHOICES = [
        ('client', 'Клиент'),
        ('employee', 'Сотрудник'),
        ('administrator', 'Администратор'),
        ('Doctor', 'Врач')
    ]
    position = models.CharField(max_length=32,
                                choices=POSITION_CHOICES,
                                default='client',
                                verbose_name='Класс пользователя',
                                help_text='По умолчанию - клиент')
    address = models.TextField(null=True,
                               blank=True,
                               verbose_name='Физический адресс клиента')
    phone = models.CharField(max_length=32,
                             unique=True,
                             verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Почта/email',
                              unique=True,
                              blank=False)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=30,
                                  blank=False)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=30,
                                 blank=False)
    patronymic = models.CharField(verbose_name='Отчество',
                                  max_length=30,
                                  blank=True,
                                  help_text='Пустое поле если отчества нет')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}, почта: {self.email}'


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
    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                verbose_name="Услугп")
    client = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Клиент')
    client_comment = models.TextField(null=True,
                                      verbose_name='Комментарий клиента')

    class Meta:
        verbose_name = 'Визит к врачу'
        verbose_name_plural = 'Визиты к врачу'

    def __str__(self):
        return f'{self.id} {self.date} {self.time} {self.client}'


class Contact(models.Model):
    address = models.CharField(max_length=256,
                               verbose_name='адрес')
    phone = models.CharField(max_length=32,
                             verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Почта/email',
                              unique=False,
                              blank=False)
    map_iframe = models.TextField(help_text="ссылка на встраивание карт")

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return f'{self.address} {self.phone}'

    def save(self, *args, **kwargs):
        if not self.id and Contact.objects.exists():  # if not self.id нужно для редактирования
            raise ValidationError('Может быть только одна модель контактов')
        return super(Contact, self).save(*args, **kwargs)


class DoctorCard(models.Model):
    image = models.ImageField(upload_to='website/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')
    name = models.CharField(max_length=128, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    specialization = models.CharField(verbose_name='специалтзация',
                                      max_length=64)

    class Meta:
        verbose_name = 'Карточка врача'
        verbose_name_plural = 'Карточки врачей'


class AboutUs(models.Model):
    image = models.ImageField(upload_to='website/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')
    title = models.CharField(max_length=128, verbose_name='Название')
    content = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def __str__(self):
        return 'о нас'

    def save(self, *args, **kwargs):
        if not self.id and AboutUs.objects.exists():  # if not self.id нужно для редактирования
            raise ValidationError('Может быть только одна модель О нас')
        return super(AboutUs, self).save(*args, **kwargs)


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
