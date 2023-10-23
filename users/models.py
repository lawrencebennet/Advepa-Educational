from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group
from advepa.models import Stand, Pavilion, Exhibition
from django.db import models
import secrets
import string
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
            # email validation
        if not email:
            raise ValueError(_('You must provide an email address'))

        super_user = self.create_user(email, username, password, **other_fields)
        return super_user

    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


def generate_unique_code():
    while True:
        random_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(5))
        if not School.objects.filter(custom_id=random_code).exists():
            return random_code.upper()


def school_directory_path(instance, filename):
    return f'{instance.custom_id}/{filename}'


class School(models.Model):
    name = models.CharField(blank=False, max_length=100, default="Nuova Scuola")
    custom_id = models.CharField(max_length=10, blank=False, default=generate_unique_code, unique=True)
    info = models.TextField(_('info'), max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    theme = models.CharField(blank=False, max_length=100, default="Default")
    modulo_ingresso = models.BooleanField(default=False)
    modulo_comunicazione_multipla = models.BooleanField(default=False)
    modulo_personalizzato_apprendimento = models.BooleanField(default=False)
    modulo_eventi = models.BooleanField(default=False)
    modulo_segreteria = models.BooleanField(default=False)
    modulo_spazio_docenti = models.BooleanField(default=False)
    modulo_classi_innovative = models.BooleanField(default=False)
    planimetry_image = models.FileField(upload_to=school_directory_path)

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return f"{self.name}, ID: {self.custom_id}"


def user_directory_path(instance, filename):
    return f'{instance.teacher.username}/{filename}'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # stands = models.ForeignKey(Stand, on_delete=models.CASCADE, blank=True, null=True)
    # exhibitions = models.ForeignKey(Exhibition, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, blank=False, unique=True)
    avatar = models.TextField(max_length=500, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Amministratore Scuola'),
        ('teacher', 'Insegnante'),
        ('student', 'Studente'),
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='student', blank=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'

    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username}"


class MediaType(models.Model):
    EXTENSION_CHOICES = (
        ('pdf', 'PDF'),
        ('mp3', 'MP3'),
        ('wma', 'WMA'),
        ('mp4', 'MP4'),
        ('jpg', 'JPG'),
        ('png', 'PNG'),
    )
    MACRO_TYPE_CHOICES = (
        ('vid', 'VIDEO'),
        ('img', 'IMMAGINE'),
        ('doc', 'DOCUMENTO'),
        ('aud', 'AUDIO'),
    )
    extension = models.CharField(max_length=100, choices=EXTENSION_CHOICES)
    macro_type = models.CharField(max_length=100, choices=MACRO_TYPE_CHOICES)
    megabyte_limit = models.IntegerField()

    def __str__(self):
        return f'{self.get_extension_display()}, megabyte limit: {self.megabyte_limit}'


class MediaFile(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    path = models.CharField(blank=False, max_length=100)
    type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    byte_space = models.FloatField(default=0)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return f'{self.name}.{self.type.extension}, {(self.byte_space / 1000):.3f} Kilobytes, caricato da: {self.teacher.username}'


class SiteLogins(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str("Accesso da parte di" + self.user.username + ", email:" + self.user.email + ", " + str(self.date))

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Site Logins"


# python manage.py createsuperuser --username lorenzo --email lorenzobennati.dev@gmail.com


# class CustomUser(AbstractUser):
#     name = models.TextField(blank=True)
#     surname = models.TextField(blank=True)
#     school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
#     admin = models.ForeignKey(School, on_delete=models.CASCADE, related_name='admins', null=True, blank=True)
#     ROLE_CHOICES = (
#         ('superadmin', 'Super Admin'),
#         ('admin', 'Amministratore Scuola'),
#         ('teacher', 'Insegnante'),
#         ('student', 'Studente'),
#     )
#     role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='student')
#
#     def __str__(self):
#         return f'{self.username}, {self.email}'


class ClassroomSkin(models.Model):
    name = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return f'{self.name}'


class Classroom(models.Model):
    TYPE_CHOICES = (
        ('lab', 'Laboratorio'),
        ('class', 'Aula')
    )
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='class')
    skin = models.ForeignKey(ClassroomSkin, on_delete=models.CASCADE, default=1)
    name = models.CharField(blank=False, max_length=100, default="Standard")
    media_files = models.ManyToManyField(MediaFile, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    room_number = models.PositiveIntegerField(default=1)

    # def save(self, *args, **kwargs):
    #     # Trova la classroom con il room_number massimo all'interno della stessa scuola
    #     max_room_number = Classroom.objects.filter(school=self.school).aggregate(models.Max('room_number'))[
    #         'room_number__max']
    #     if max_room_number is not None:
    #         self.room_number = max_room_number + 1
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_type_display()}: {self.name}, Skin: {self.skin}, {self.media_files.count()} Files Caricati'


# Gestore di segnali per eliminare il file multimediale associato quando un record MediaFile viene eliminato
@receiver(pre_delete, sender=MediaFile)
def delete_mediafile(sender, instance, **kwargs):
    # Elimina il file multimediale dal sistema di archiviazione
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
