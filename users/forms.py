from django import forms
from users.models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from .models import *
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    username = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password1',
            'password2',
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Add User Form
class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=False)
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Amministratore Scuola'),
        ('teacher', 'Insegnante'),
        ('student', 'Studente'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'name',
            'last_name',
            'role',
            'groups',
            'school',
            'about',
            'is_active',
            'password1',
            'password2',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    username = forms.CharField(required=False)
    name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Amministratore Scuola'),
        ('teacher', 'Insegnante'),
        ('student', 'Studente'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'role',
            'name',
            'last_name',
            'school',
            'groups',
            'about',
            'is_active',
        )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class FaqForm(forms.ModelForm):
    question = forms.CharField(required=True)
    answer = forms.CharField(required=True)
    link = forms.CharField(required=False)

    class Meta:
        model = Faq
        fields = ('question', 'answer', 'link', 'section')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FaqForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['section'].queryset = FaqSection.objects.filter(school=user.school)


class NoticeForm(forms.ModelForm):
    title = forms.CharField(required=True)

    class Meta:
        model = Notice
        fields = ('title', 'text', 'link', 'meet_link', 'media_file')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NoticeForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['media_file'].queryset = MediaFile.objects.filter(teacher__school=user.school)


# class NoticeForm(forms.ModelForm):
#     title = forms.CharField(required=True)
#     text = forms.CharField(required=False)
#     link = forms.CharField(required=False)
#     meet_link = forms.CharField(required=False)
#     media_file = forms.ModelChoiceField(
#         queryset=MediaFile.objects.none(),
#         required=False
#     )
#
#     class Meta:
#         model = Notice
#         fields = ('title', 'text', 'link', 'type', 'meet_link', 'media_file')
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(NoticeForm, self).__init__(*args, **kwargs)
#
#         if user:
#             self.fields['media_file'].queryset = MediaFile.objects.filter(teacher__school=user.school)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         notice_type = cleaned_data.get('type')
#
#         if notice_type == 'news':
#             if not cleaned_data.get('text'):
#                 self.add_error('text', "Questo campo è obbligatorio per l'avviso di tipo 'news'.")
#         elif notice_type == 'doc':
#             if not cleaned_data.get('media_file'):
#                 self.add_error('media_file', "Questo campo è obbligatorio per l'avviso di tipo 'doc'.")
#         elif notice_type == 'meet':
#             if not cleaned_data.get('meet_link'):
#                 self.add_error('meet_link', "Questo campo è obbligatorio per l'avviso di tipo 'meet'.")
#
#         return cleaned_data


# class NoticeForm(forms.ModelForm):
#     title = forms.CharField(required=True)
#
#     class Meta:
#         model = Notice
#         fields = ('title', 'text', 'media_file', 'link', 'meet_link')
#
#
# class MeetNoticeForm(forms.ModelForm):
#     title = forms.CharField(required=True)
#     meet_link = forms.CharField(required=True)
#
#     class Meta:
#         model = Notice
#         fields = ('title', 'meet_link', 'school')
#
#
# class NewsNoticeForm(forms.ModelForm):
#     title = forms.CharField(required=True)
#     question = forms.CharField(required=True)
#     link = forms.CharField(required=False)
#
#     class Meta:
#         model = Notice
#         fields = (
#             'title', 'question', 'link', 'school')
#
#
# class DocNoticeForm(forms.ModelForm):
#     title = forms.CharField(required=True)
#     link = forms.CharField(required=False)
#     media_file = forms.ModelChoiceField(
#         queryset=MediaFile.objects.none(),
#         required=True
#     )
#
#     class Meta:
#         model = Notice
#         fields = ('title', 'media_file', 'link')
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(DocNoticeForm, self).__init__(*args, **kwargs)
#
#         if user:
#             self.fields['media_file'].queryset = MediaFile.objects.filter(teacher__school=user.school)
#
#     def save(self, commit=True):
#         notice = super(DocNoticeForm, self).save(commit=commit)
#         return notice


class SchoolForm(forms.ModelForm):
    name = forms.CharField(required=True)
    custom_id = forms.CharField(required=True)
    info = forms.CharField(required=False)
    theme = forms.CharField(required=False)
    listening_desk = forms.CharField(required=False)

    class Meta:
        model = School
        fields = (
            'name', 'listening_desk', 'custom_id', 'info', 'is_active', 'theme', 'modulo_ingresso',
            'modulo_comunicazione_multipla',
            'modulo_personalizzato_apprendimento', 'modulo_eventi', 'modulo_segreteria', 'modulo_spazio_docenti',
            'modulo_classi_innovative',
        )


class EditSchoolForm(forms.ModelForm):
    name = forms.CharField(required=True)
    custom_id = forms.CharField(required=True)
    info = forms.CharField(required=False)
    theme = forms.CharField(required=False)
    listening_desk = forms.CharField(required=False)

    class Meta:
        model = School
        fields = (
            'name', 'custom_id', 'listening_desk', 'info', 'is_active', 'theme', 'modulo_ingresso',
            'modulo_comunicazione_multipla',
            'modulo_personalizzato_apprendimento', 'modulo_eventi', 'modulo_segreteria', 'modulo_spazio_docenti',
            'modulo_classi_innovative',
        )


class EditSchoolAdminForm(forms.ModelForm):
    name = forms.CharField(required=True)
    custom_id = forms.CharField(required=False)
    info = forms.CharField(required=False)
    theme = forms.CharField(required=False)
    listening_desk = forms.CharField(required=False)

    class Meta:
        model = School
        fields = (
            'name', 'custom_id', 'info', 'theme', 'listening_desk'
        )


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


# class EmailValidationOnForgotPassword(PasswordResetForm):
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if not CustomUser.objects.filter(email__iexact=email, is_active=True).exists():
#             raise forms.ValidationError("There is no user registered with the specified email address!")
#         return email


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class PermissionsForm(forms.ModelForm):
    name = forms.CharField(label='Name', help_text="Example: Can action modelname")
    codename = forms.CharField(label='Code Name', help_text="Example: action_modelname")

    class Meta:
        model = Permission
        fields = ('name', 'codename', 'content_type')


class UserPermissionsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('user_permissions',)


# UPLOAD FILE FORM
class UploadMediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ('file',)  # Includi solo il campo del file nel modulo

    def save(self, commit=True):
        media_file = super().save(commit=False)
        media_file.teacher = self.user
        file_extension = media_file.file.name.split('.')[-1]
        try:
            media_type = MediaType.objects.get(extension=file_extension)
            if media_file.file.size / 1000000 > media_type.megabyte_limit:
                self.add_error('file',
                               f"Dimensioni del file '{file_extension}' troppo grandi! Massima dimensione {media_type.megabyte_limit}mb")
                # raise forms.ValidationError(f"Dimensioni del file '{media_file.file.size / 1000}' MB troppo grandi!")
            media_file.type = media_type
        except MediaType.DoesNotExist:
            # raise forms.ValidationError(f"Tipo di file '{file_extension}' non supportato")
            self.add_error('file', f"Tipo di file '{file_extension}' non supportato")
            self.has_error(True)
            return
        media_file.name = media_file.file.name.split('.')[0]
        media_file.byte_space = media_file.file.size
        if commit:
            media_file.save()
        return media_file


# FORMS PER IL DASHBOARD ADMIN DI DJANGO
class MediaFileFormCreate(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file']


class MediaFileFormView(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'
