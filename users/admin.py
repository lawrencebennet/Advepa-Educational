from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.contrib import admin
from django.http import HttpResponseBadRequest
from .models import *
from .forms import *

admin.site.register(School)
admin.site.register(CustomUser)
admin.site.register(Classroom)
admin.site.register(ClassroomSkin)


class MediaFileAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            # Utilizza il form di creazione quando si crea un nuovo oggetto
            return MediaFileFormCreate
        else:
            # Utilizza il form di visualizzazione quando si modifica o visualizza un oggetto esistente
            return MediaFileFormView

    def save_model(self, request, obj, form, change):
        # Assegna il campo 'teacher' all'utente attualmente connesso
        obj.teacher = request.user

        # Calcola il percorso e il nome del file
        obj.path = obj.file.url
        obj.name = obj.file.name.split('.')[0]

        # Calcola lo spazio occupato in megabyte
        obj.byte_space = obj.file.size

        # Trova il tipo di file corrispondente
        file_extension = obj.file.name.split('.')[1]
        try:
            obj.type = MediaType.objects.get(extension=file_extension)
            if obj.byte_space / 1000000 > obj.type.megabyte_limit:
                return HttpResponseBadRequest(f"Dimensioni del file '{obj.byte_space / 1000}'MB troppo grandi!")
        except MediaType.DoesNotExist:
            return HttpResponseBadRequest(f"Tipo di file '{file_extension}' non supportato")

        # Salva l'oggetto MediaFile nel database
        super().save_model(request, obj, form, change)


admin.site.register(MediaType)
admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(Notice)
admin.site.register(Faq)
admin.site.register(FaqSection)
