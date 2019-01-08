from django.db import models
# from django.core.validators import FileExtensionValidator

import uuid

from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

from .validators import FileValidator

from django_clamd.validators import validate_file_infection


class ContactAdminStatus(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Статус ответа администратора'   #Admin response status
        verbose_name_plural = 'Статусы ответа администратора' #Admin response statuses


class ContactResponseAbstract(models.Model):
    email = models.EmailField(verbose_name="email получателя")  #email recipient
    message = models.TextField(blank=True, verbose_name="Текст сообщения")  #Message text
    attach = models.FileField(upload_to='contact/%Y/', blank=True, null=True,
                              verbose_name="Файл вложения", #Attachment file
                              validators=[validate_file_infection, ],)
    # status = models.BooleanField(editable=False, verbose_name="Отправлено")

    creation_datetime = models.DateTimeField(verbose_name="Дата ответа", auto_now_add=True) #Reply date
    update_datetime = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)   #Update Date

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        abstract = True


class ContactAdminResponse(ContactResponseAbstract):
    RESPONSE_TYPE_CHOICES = (
        ('R', 'Ответ'), #Answer
        ('F', 'Перенаправление'), #Redirection
    )

    type = models.CharField(max_length=1, choices=RESPONSE_TYPE_CHOICES, verbose_name="Тип", default='R')

    class Meta:
        verbose_name = 'Ответ администратора'   #Admin response
        verbose_name_plural = 'Ответы администратора'   #Admin responses


class ContactAbstract(models.Model):

    POST_CHOICES = (
        ('R', 'Руководитель компании'), #Director of company
        ('P', 'Представитель компании'),    #Representative of the company
        ('I', 'Индивидуальный предприниматель'),
        ('Z', 'Инженер компании'),
        ('G', 'Государственный служащий'),
        ('F', 'Гражданин РФ'),
        ('S', 'Студент'),
        ('E', 'Пенсионер'),
        ('O', 'Общественный деятель'),
        ('C', 'Представитель СРО'),
        ('D', 'Депутат'),
        ('C', 'Судья'),
        ('U', 'Представитель прокуратуры'),
        ('M', 'Представитель органов МВД / ФСБ'),
        ('N', 'Представитель налоговой службы'),
        ('A', 'Другое'),
    )

    surname = models.CharField(max_length=255, verbose_name="Фамилия")     #Surname
    name = models.CharField(max_length=255, verbose_name="Имя")
    patronymic = models.CharField(max_length=255, verbose_name="Отчество", blank=True, null=True)
    phone = PhoneNumberField(verbose_name="номер телефона") #phone number
    email = models.EmailField(verbose_name="email адрес")

    post = models.CharField(max_length=1, verbose_name="Должность / социальное положение",  #Position / social status
                            choices=POST_CHOICES, default='P')
    work_place = models.TextField(max_length=2000, verbose_name="Место работы", blank=True, null=True)  #Place of work
    file = models.FileField(upload_to='contact/%Y/',
                            blank=True, null=True,
                            # validators=[FileExtensionValidator(allowed_extensions=['.pdf', '.doc', '.docx', '.xlsx',
                            #                                                        '.xls'])],
                            validators=[FileValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls', 'jpg',
                                                                          'png', 'zip', 'rar'],
                                                      max_size=20 * 1024 * 1024,
                                                      ),
                                        validate_file_infection],
                            verbose_name="Файл вложения (не более 20 мб)")  #Attachment file (no more than 20 Mb)
    message = models.TextField(blank=True, verbose_name="Текст сообщения")  #Message text

    creation_datetime = models.DateTimeField(verbose_name="Дата поступления", auto_now_add=True)    #receipt date
    update_datetime = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)   #Update Date

    def __str__(self):
        return 'Обращение {}'.format(self.id)   #Appeal {}

    @property
    def full_name(self):
        full_name = '{} {}'.format(self.surname, self.name)
        if self.patronymic:
            full_name += ' {}'.format(self.patronymic)

        return full_name

    class Meta:
        abstract = True


class ContactAdmin(ContactAbstract):
    CONTACT_CHOICES = (
        ('A', 'Руководителю компании'), #The head of the company
        ('E', 'Администратору сайта'),  #Site Administrator
    )

    response = models.OneToOneField(ContactAdminResponse, verbose_name="Ответ", blank=True, null=True)  #Answer

    status = models.ForeignKey(ContactAdminStatus, blank=True, null=True, default=1, verbose_name="Статус обращения") #Treatment status

    contact_choice = models.CharField(max_length=1, choices=CONTACT_CHOICES,
                                      verbose_name="Кому адресовано", default='А') #To whom is it addressed?

    @property
    def get_admin_url(self):
        return reverse('admin-contact-detail', args=[self.pk, ])

    class Meta:
        verbose_name = 'Обращение к администратору' #Contact the administrator
        verbose_name_plural = 'Обращения к администратору' #Appeals to the administrator


class ContactExpertStatus(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")   #Title

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Статус ответа эксперта' #Expert Answer Status
        verbose_name_plural = 'Статусы ответа эксперта' #Expert response statuses


class ContactExpertResponse(ContactResponseAbstract):
    class Meta:
        verbose_name = 'Ответ эксперта админа'  #Admin expert answer
        verbose_name_plural = 'Ответы эксперта админа'  #Admin expert answers


class Expert(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Эксперт'    #Expert
        verbose_name_plural = 'Эксперты'    #Experts


class ContactExpert(ContactAbstract):
    # SUBJECT_TYPE_CHOICES = (
    #     ('R', 'Другое'),
    # )

    @property
    def get_admin_url(self):
        return reverse('expert-contact-change_status', args=[self.pk,])

    response = models.OneToOneField(ContactExpertResponse, verbose_name="Ответ", blank=True, null=True) #Answer

    # subject = models.CharField(max_length=1, choices=SUBJECT_TYPE_CHOICES, verbose_name="Тема обращения", default='R')

    status = models.ForeignKey(ContactExpertStatus, blank=True, null=True, default=1, verbose_name="Статус обращения")  #Treatment status

    class Meta:
        verbose_name = 'Обращение к эксперту'   #Appeal to the expert
        verbose_name_plural = 'Обращения к эксперту'    #Appeal to the expert


class ExpertResponse(models.Model):
    subject = models.CharField(max_length=1000, verbose_name="Тема")    #Theme
    text = models.TextField(verbose_name="Ответ")   #Answer
    response_date = models.DateTimeField(blank=True, null=True, verbose_name="дата ответа") #response date
    file = models.FileField(upload_to='expert_responses/%Y/',
                            blank=True, null=True,
                            validators=[validate_file_infection, ],
                            verbose_name="приложить файл")  #attach file
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # TODO check for unique&
    expert = models.ForeignKey(Expert)
    contact_expert_question = models.ForeignKey(ContactExpert, related_name="expertresponse",
                                                verbose_name="ответ экспертов") #expert response

    def __str__(self):
        return '{} / {}'.format(self.subject, self.expert)

    class Meta:
        verbose_name = 'Ответ эксперта' #Expert answer
        verbose_name_plural = 'Ответы эксперта' #Expert answers
