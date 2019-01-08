from django.db import models
from django.contrib.auth.models import AbstractUser

from smart_selects.db_fields import ChainedForeignKey


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Region(models.Model):
    name = models.CharField(max_length=255)


class City(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=250)


class ClientInfo(models.Model):
    DOLZNOST_CHOICES = (

    # Управляющий партнёр;
    # Генеральный директор;
    # Директор;
    # Заместитель генерального директора / директора;
    # Руководитель департамента / отдела / структурного подразделения;
    # Руководитель проекта;
    # Начальник участка / отдела;
    # Главный инженер;
    # Главный инженер проекта;
    # Прораб;
    # Мастер;
    # Инженер;
    # Специалист;
    # Менеджер;
    # Юрист;
    # Юрисконсульт;
    # Представитель компании по доверенности.

        (1, 'Собственник бизнеса'), #Business owner
        (2, 'Генеральный директор'),    #CEO
        (3, 'Директор'),    #Director
        (4, 'Заместитель генерального директора / директора'),
        (5, 'Руководитель департамента / отдела / структурного подразделения'),
        (6, 'Руководитель проекта'),
        (7, 'Начальник участка / отдела'),
        (9, 'Главный инженер'),
        (10, 'Главный инженер проекта'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # username
    # naimenovanie_kompanii_ili_FIO = models.CharField(max_length=200, blank=True,
    #                                                  null=True, help_text="Полное наименование организации")
    kratkoe_naimenovanie_kompanii = models.CharField(max_length=200, blank=True,
                                                     null=True, help_text="Краткое наименование организации")   #Short name of the organization
    yuradres_registracii_kompanii = models.TextField(blank=True,
                                                     null=True, help_text="Адрес регистрации организации (юридический)")    #Address of registration of the organization (legal)
    pochtovyi_faktadres_kompanii = models.TextField(blank=True,
                                                    null=True, help_text="Фактический (почтовый) адрес организации")    #The actual (postal) address of the organization
    subject_RF = models.ForeignKey(Region,
                                   help_text="Субъект РФ и район деятельности организации " #The subject of the Russian Federation and the area of the organization
                                   "(место производства, склада, цеха, базы, офиса, выставочного зала)")    #(place of production, warehouse, workshop, base, office, exhibition hall)
    naselennyi_punkt = ChainedForeignKey(
        Region,
        chained_field="subject_RF",
        chained_model_field="subject_RF",
        show_all=False,
        auto_choose=True,
        sort=True,
        help_text="Город, городское поселение и ближайшие населенные пункты, расположенные на удалении 30 км. " #City, city settlement and the nearest populated areas located at a distance of 30 km.
                  "от фактического адреса расположения офиса/производственной базы/цеха/склада/магазина/и пр.)" #from the actual address of the location of the office / production base / shop / warehouse / store / etc.
    )
    fio_rukovoditelya_kompanii = models.TextField(blank=True, null=True,
                                                  help_text="Ф.И.О. руководителя организации (генерального директора / директора)") #FULL NAME. head of organization (general director / director)
    fio_polzovatelya_lich_cab = models.TextField(blank=True, null=True,
                                                  help_text="Ф.И.О. основного пользователя сервисами портала ЕСТЗ - "   #FULL NAME. main user services portal portal ESTZ
                                                            "физическое лицо / представителя юр.лица / "    #individual / representative of legal entity 
                                                            "индивидуального предпринимателя "  #individual entrepreneur
                                                            "(владелец личного кабинета на портале") #owner of personal account on the portal
    dolgnost_post_polzovatelya = models.CharField(max_length=200, blank=True, null=True,
                                                  choices=DOLZNOST_CHOICES,
                                                  help_text="Должность основного пользователя сервисами портала ЕСТЗ"   #Position of the main user by the services of the ESTP portal
                                                             " - физического лица / представителя юр.лица / "   #- physical person / representative of legal entity /
                                                             "индивидуального предпринимателя " #individual entrepreneur
                                                             "(владельца личного кабинета на портале)") #(owner of personal account on the portal)
    # nomer_telefona_kompanii
    # e_mail_kompanii
    # nomer_telefona_polzovatelya
    # oGRN_kompanii
    # iNN_kompanii
    # vid_uslug_i_rabot_kompanii
    # specializaciy_uslug_i_rabot
    # # email_polzovatelya
    # prochie_kontaktnye_svedeniy
    # data_registracii_na_site
    # # Login_polzovatelya
    # # Parole_polzovatelya
    # kolichestvo_podannyh_zayvok
    # kolichestvo_postupivshih_na_rassmotrenie_zayvok
    # kolichestvo_otkazov_ot_rassmotraniy_zayvok
    # kolichestvo_neotrabzayvok
    # kolichestvo_uspehotrabzayvok
    # dokument
    # status_polzovatelya
    # status_oplaty
    # status_polzovatelya
    # ip_adres_polzovatelya
    # sdres_site_kompanii
    # foto_avatar
