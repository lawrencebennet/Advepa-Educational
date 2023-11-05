import json
from datetime import datetime, timedelta

import requests
from django.db.models import Max, Min
from django.urls import reverse
from django.utils import timezone
from users.models import *
from advepa.forms import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from users.models import CustomUser

from users.forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import render


@login_required(login_url='advepa:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Aggiornata Correttamente')
            return redirect('/password/')
        else:
            messages.warning(request, 'Form non valido')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'advepa/modules/change-password.html', {'form': form, "page_title": "Modifica Password"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def users(request):
    if request.user.role == 'admin':
        user_list = CustomUser.objects.filter(school=request.user.school).order_by('-role')
    else:
        user_list = CustomUser.objects.filter().order_by('-is_superuser', 'role')
    paginator = Paginator(user_list, 7)  # Mostra 7 utenti per pagina
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Utenti"
    }
    return render(request, "advepa/modules/users.html", context)


def create_unique_username(name, last_name):
    # Crea un 'username' unico basato su 'name' e 'last_name'
    base_username = f"{name.lower()}{last_name.lower()}"
    username = base_username
    count = 1

    while CustomUser.objects.filter(username=username).exists():
        # Se il 'username' esiste già, aggiungi un numero all'username
        username = f"{base_username}{count}"
        count += 1

    return username


@login_required(login_url='advepa:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            if not form.cleaned_data.get('school'):
                form.instance.school = request.user.school
            if not form.cleaned_data.get('username'):
                name = form.cleaned_data.get('name')
                last_name = form.cleaned_data.get('last_name')
                unique_username = create_unique_username(name, last_name)
                form.instance.username = unique_username

            user_obj = form.save()
            user_obj.groups.clear()
            for i in form.cleaned_data.get('groups'):
                user_obj.groups.add(i)
            messages.success(request, f"L'utente {user_obj.username} è stato creato con successo!")
            return redirect('advepa:users')
    else:
        form = CustomUserForm()
        if request.user.role == 'admin':
            form.fields['role'].choices = [(value, label) for value, label in form.fields['role'].choices if
                                           value not in ['admin', 'superadmin']]
    return render(request, 'advepa/modules/add-user.html', {'form': form, "page_title": "Crea Utente"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            user_obj.groups.clear()
            for i in form.cleaned_data['groups']:
                user_obj.groups.add(i)
            return redirect('advepa:users')
    else:
        form = EditUserForm(instance=user_obj)
    status = "Modifica"
    return render(request, 'advepa/modules/add-user.html',
                  {'form': form, 'status': status, "page_title": "Modifica Utente"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def user_details(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    context = {
        "user_obj": user_obj,
        "user_group_perms": user_obj.get_group_permissions(),
        "user_perms": user_obj.get_user_permissions(),
        "page_title": "Dettagli account"
    }

    return render(request, "advepa/modules/user-details.html", context)


@login_required(login_url='advepa:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_user(request, id):
    u = CustomUser.objects.get(id=id)
    u.delete()
    messages.success(request, "Utente eliminato correttamente!")
    return redirect('advepa:users')


@login_required(login_url='advepa:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_user(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomUser.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Utenti eliminati con successo!'})
    response.status_code = 200
    return response


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None and user.is_active:
                login(request, user)
                SiteLogins.objects.create(**{'user': user})
                if not check_school_setted(request) and not (
                        request.user.is_superuser or request.user.role == "superadmin"):
                    return redirect('advepa:page-error-403')
                if request.user.is_superuser or request.user.role in ['superadmin', 'admin']:
                    mex = "Benvenuto nella dashboard di amministrazione"
                elif request.user.role == "teacher":
                    mex = f'Benvenuto alla Dashboard Insegnanti'
                else:
                    return redirect('advepa:page-error-403')
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    messages.success(request, mex)
                    return redirect('advepa:dashboard')
            else:
                messages.warning(request, "Attenzione! L'utente non è attivo")
        else:
            messages.warning(request, 'Attenzione! Username o password non corretti')
            return render(request, 'advepa/modules/login.html', context={'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('advepa:dashboard')
        form = LoginForm()
    return render(request, 'advepa/modules/login.html', context={'form': form})


def check_school_setted(request):
    return True if ((request.user.role == 'admin' or request.user.role == 'teacher') and request.user.school) else False


def logout_user(request):
    logout(request)
    messages.success(request, 'Logout eseguito correttamente!')
    return redirect('advepa:login')


@login_required(login_url='advepa:login')
@permission_required({'auth.view_group'}, raise_exception=True)
def groups_list(request):
    context = {
        "groups": Group.objects.annotate(user_count=Count('customuser', distinct=True)).annotate(
            perms_count=Count('permissions', distinct=True)),
        "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
        "page_title": "Gruppi"
    }

    return render(request, 'advepa/modules/group-list.html', context)


@login_required(login_url='advepa:login')
@permission_required({'auth.view_group', 'auth.change_group'}, raise_exception=True)
def group_edit(request, id):
    group_obj = get_object_or_404(Group, id=id)

    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict)

        try:
            group_obj.name = data['name'][0]
            group_obj.save()
        except:
            response = JsonResponse({"error": "Group Name already exist"})
            response.status_code = 403
            return response

        if 'permissions[]' in data:
            group_obj.permissions.clear()
            group_obj.permissions.set(data['permissions[]'])
        else:
            group_obj.permissions.clear()

        response = JsonResponse({"success": "Save Successfully"})
        response.status_code = 200
        return response

    else:
        form = GroupForm(instance=group_obj)

    return render(request, 'advepa/modules/group-edit.html', {'form': form, "page_title": "Modifica Gruppi"})


@login_required(login_url='advepa:login')
@permission_required({'auth.view_group', 'auth.delete_group'}, raise_exception=True)
def group_delete(request, id):
    g = get_object_or_404(Group, id=id)
    g.delete()
    messages.success(request, 'Group Deleted Sucessfully')
    return redirect('advepa:groups')


@login_required(login_url='advepa:login')
@permission_required({'auth.view_group', 'auth.add_group'}, raise_exception=True)
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group Created Successfully')
            return redirect('advepa:groups')
        else:
            messages.warning(request, 'Name Already Exist')
            return render(request, 'advepa/modules/group-add.html', {'form': form, 'page_title': 'Add Group'})
    else:
        form = GroupForm()
        return render(request, 'advepa/modules/group-add.html', {'form': form, "page_title": "Add Group"})


@login_required(login_url='advepa:login')
@permission_required({'auth.view_permission'}, raise_exception=True)
def permissions(request):
    permission_list = Permission.objects.all()
    paginator = Paginator(permission_list, 5)  # Show 5 permission per page.
    context = {
        "permissions_obj": paginator.get_page(request.GET.get('page')),
        "page_title": "Permessi"
    }

    return render(request, 'advepa/modules/permissions.html', context)


@login_required(login_url='advepa:login')
@permission_required({'auth.view_permission', 'auth.change_permission'}, raise_exception=True)
def edit_permissions(request, id):
    perm_obj = get_object_or_404(Permission, id=id)
    if request.method == 'POST':
        form = PermissionsForm(request.POST, instance=perm_obj)
        if form.is_valid():
            form.save()
            return redirect('advepa:permissions')
    else:
        form = PermissionsForm(instance=perm_obj)
        return render(request, 'advepa/modules/edit-permissions.html',
                      {'form': form, "page_title": "Modifica Permessi"})


@login_required(login_url='advepa:login')
@permission_required({'auth.view_permission', 'auth.delete_permission'}, raise_exception=True)
def delete_permissions(request, id):
    perm_obj = get_object_or_404(Permission, id=id)
    perm_obj.delete()
    messages.success(request, 'Permission Delete Successfully')
    return redirect('advepa:permissions')


@login_required(login_url='advepa:login')
@permission_required({'auth.view_permission', 'auth.add_permission', 'auth.change_permission'}, raise_exception=True)
def assign_permissions_to_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict)

        if 'user_permissions[]' in data:
            user_obj.user_permissions.clear()
            user_obj.user_permissions.set(data['user_permissions[]'])
        else:
            user_obj.user_permissions.clear()
        response = JsonResponse({"success": "Save Successfully"})
        response.status_code = 200
        return response

    else:
        form = UserPermissionsForm(instance=user_obj)
    return render(request, 'advepa/modules/assign_permissions_to_user.html',
                  {'form': form, "page_title": "Assign Permissions"})




@login_required(login_url='advepa:login')
@permission_required({'users.view_notice', 'users.change_notice'}, raise_exception=True)
def edit_notice(request, id):
    notice_obj = get_object_or_404(Notice, id=id)
    notice_type = notice_obj.type
    if notice_type == "meet":
        type_title = "Appuntamento"
    elif notice_type == "doc":
        type_title = "Bandi"
    elif notice_type == "news":
        type_title = "News"
    else:
        type_title = "Elemento in bacheca"
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice_obj)
        if form.is_valid():
            notice_obj = form.save()
            messages.success(request, f'Elemento "{notice_obj.title}" modificato con successo!')
            return redirect('advepa:school-dashboard')
    else:
        form = NoticeForm(instance=notice_obj)
    status = "Modifica"

    return render(request, 'advepa/modules/add-notice.html',
                  {'form': form, 'status': status, "page_title": "Modifica Elemento in bacheca",
                   'notice_type': notice_type, 'type_title': type_title})


@login_required(login_url='advepa:login')
@permission_required({'users.view_faq', 'users.add_faq'}, raise_exception=True)
def add_notice(request, notice_type=None):
    if notice_type:
        if notice_type == "meet":
            type_title = "Appuntamento"
        elif notice_type == "doc":
            type_title = "Bandi"
        elif notice_type == "news":
            type_title = "News"
        else:
            type_title = "Elemento in bacheca"
        notice_count = Notice.objects.filter(school=request.user.school, type=notice_type).count()
        if notice_type == 'meet' and length >= 1:
            messages.warning(request, f"Impossibile creare! Esiste già 1 appuntamento meet in bacheca!")
            return redirect('advepa:school-dashboard')
        elif notice_count >= 10:
            messages.warning(request, f"Impossibile creare! Esistono già 10 {type_title} in bacheca!")
            return redirect('advepa:school-dashboard')
        if request.method == 'POST':
            form = NoticeForm(request.POST, user=request.user)
            if form.is_valid():
                if not form.cleaned_data.get('school'):
                    form.instance.school = request.user.school
                if not form.cleaned_data.get('notice_type'):
                    form.instance.type = notice_type
                notice_obj = form.save()
                messages.success(request, f"Elemento in bacheca aggiunto con successo")
                return redirect('advepa:school-dashboard')
        else:
            form = NoticeForm(user=request.user)

        return render(request, 'advepa/modules/add-notice.html',
                      {'form': form, "page_title": "Crea elemento in bacheca", "notice_type": notice_type,
                       "type_title": type_title})
    else:
        messages.warning(request, f"Tipo di elemento in bacheca non specificato per la creazione")
        return redirect('advepa:school-dashboard')


@login_required(login_url='advepa:login')
@permission_required({'users.view_notice', 'users.delete_notice'}, raise_exception=True)
def delete_notice(request, id):
    u = Notice.objects.get(id=id)
    u.delete()
    messages.success(request, "Elemento rimosso correttamente dalla bacheca!")
    return redirect('advepa:school-dashboard')


@login_required(login_url='advepa:login')
@permission_required({'users.view_faq', 'users.add_faq'}, raise_exception=True)
def add_faq(request):
    if request.method == 'POST':
        form = FaqForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Faq aggiunta con successo")
            return redirect('advepa:school-dashboard')
    else:
        form = FaqForm(user=request.user)
    return render(request, 'advepa/modules/add-faq.html', {'form': form, "page_title": "Crea Faq"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_faq', 'users.change_faq'}, raise_exception=True)
def edit_faq(request, id):
    faq_obj = get_object_or_404(Faq, id=id)
    if request.method == 'POST':
        form = FaqForm(request.POST, instance=faq_obj)
        if form.is_valid():
            faq_obj = form.save()
            messages.success(request, f'Faq "{faq_obj.question}" modificata con successo!')
            return redirect('advepa:school-dashboard')
    else:
        form = FaqForm(instance=faq_obj)
    status = "Modifica"
    return render(request, 'advepa/modules/add-faq.html',
                  {'form': form, 'status': status, "page_title": "Modifica Faq"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_faq', 'users.delete_faq'}, raise_exception=True)
def delete_faq(request, id):
    u = Faq.objects.get(id=id)
    u.delete()
    messages.success(request, "Faq eliminata correttamente!")
    return redirect('advepa:school-dashboard')


@login_required(login_url='advepa:login')
@permission_required({'users.view_school'}, raise_exception=True)
def schools(request):
    school_list = School.objects.filter().order_by('name')
    paginator = Paginator(school_list, 7)  # Mostra 7 utenti per pagina
    context = {
        "school_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Scuole"
    }
    return render(request, "advepa/modules/schools.html", context)


@login_required(login_url='advepa:login')
@permission_required({'users.view_school', 'users.add_school'}, raise_exception=True)
def add_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            school_obj = form.save()
            messages.success(request, f"La scuola {school_obj} è stata creata con successo!")
            return redirect('advepa:schools')
    else:
        initial_data = {'custom_id': generate_unique_code()}  # Imposta il valore predefinito per custom_id
        form = SchoolForm(initial=initial_data)
    return render(request, 'advepa/modules/add-school.html', {'form': form, "page_title": "Crea Scuola"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_school', 'users.change_school'}, raise_exception=True)
def edit_school(request, id):
    school_obj = get_object_or_404(School, id=id)
    if request.method == 'POST':
        if request.user.role == "admin":
            form = EditSchoolAdminForm(request.POST, request.FILES, instance=school_obj)
        else:
            form = EditSchoolForm(request.POST, request.FILES, instance=school_obj)

        if form.is_valid():
            school_obj = form.save()
            messages.success(request, f"La scuola {school_obj} è stata modificata con successo!")
            return redirect('advepa:schools')
    else:
        if request.user.role == "admin":
            form = EditSchoolAdminForm(instance=school_obj)
        else:
            form = EditSchoolForm(instance=school_obj)
    status = "Modifica"
    return render(request, 'advepa/modules/add-school.html',
                  {'form': form, 'status': status, "page_title": "Modifica Scuola"})


@login_required(login_url='advepa:login')
def school_dashboard(request, school_id=None):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom-select')
        file_id = request.POST.get('file-select')
        classroom = Classroom.objects.get(pk=classroom_id)
        media_file = MediaFile.objects.get(pk=file_id)
        # Aggiungi il file alla classe utilizzando la relazione many-to-many
        classroom.media_files.add(media_file)
        # Salva l'istanza della classe
        classroom.save()
    if request.user.school:
        school = request.user.school
    elif school_id:
        school = School.objects.get(custom_id=school_id)
    else:
        context = {
            "school": None,
            "classroom_list": None,
            "uploaded_file_list": None,
            "all_file_list": None,
            "page_title": "Dashboard Scuola",
        }
        return render(request, 'advepa/school-dashboard.html', context)

    # Trova le classi collegate alla stessa scuola dell'utente
    classrooms = Classroom.objects.filter(school=school)
    # Trova i file collegati a queste classi
    uploaded_file_list = MediaFile.objects.filter(classroom__in=classrooms, teacher=request.user).order_by(
        '-create_date').distinct()
    all_file_list = MediaFile.objects.filter(teacher=request.user).order_by('-create_date')
    paginator = Paginator(uploaded_file_list, 7)  # Mostra 7 file per pagina

    faq_section_1 = FaqSection.objects.filter(school=school, area_id='1').first()
    faq_section_2 = FaqSection.objects.filter(school=school, area_id='2').first()
    faq_section_3 = FaqSection.objects.filter(school=school, area_id='3').first()

    news = Notice.objects.filter(school=school, type='news').order_by('-last_modify_date')
    docs = Notice.objects.filter(school=school, type='doc').order_by('-last_modify_date')
    meet = Notice.objects.filter(school=school, type='meet').first()
    context = {
        "school": school,
        "classroom_list": classrooms,
        "uploaded_file_list": paginator.get_page(request.GET.get('page')) if paginator else None,
        "all_file_list": all_file_list,
        "page_title": "Dashboard Scuola",
        "faq_section_1": faq_section_1,
        "faq_section_2": faq_section_2,
        "faq_section_3": faq_section_3,
        'news': news,
        'docs': docs,
        'meet': meet
    }
    return render(request, 'advepa/school-dashboard.html', context)


@login_required(login_url='advepa:login')
@permission_required({'users.view_school', 'users.delete_school'}, raise_exception=True)
def delete_school(request, id):
    u = School.objects.get(id=id)
    u.delete()
    messages.success(request, "Scuola eliminata correttamente!")
    return redirect('advepa:schools')


@login_required(login_url='advepa:login')
@permission_required({'users.view_school', 'users.delete_school'}, raise_exception=True)
def delete_multiple_school(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        school_obj = School.objects.get(pk=id)
        school_obj.delete()
    response = JsonResponse({"success": 'Scuole eliminate con successo!'})
    response.status_code = 200
    return response


# FILE MANAGER
@login_required(login_url='advepa:login')
def file_manager(request):
    if request.method == 'POST':
        form = UploadMediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.user = request.user
            media_file = form.save()
            # Verifica se ci sono errori associati al campo 'file' nel form
            if form.errors:
                if 'file' in form.errors:
                    messages.warning(request, form.errors['file'])
                else:
                    messages.warning(request, "Errore inaspettato nel caricamento del file!")
            else:
                messages.success(request, "File caricato con successo")
    else:
        form = UploadMediaFileForm()

    file_list = MediaFile.objects.filter(teacher=request.user).order_by('-create_date')
    paginator = Paginator(file_list, 7)  # Mostra 7 file per pagina

    context = {
        "form": form,
        "file_list": paginator.get_page(request.GET.get('page')),
        "page_title": "File Manager"
    }

    return render(request, 'advepa/modules/file-manager.html', context)


@login_required(login_url='advepa:login')
def delete_file(request, file_id):
    f = MediaFile.objects.get(id=file_id)
    f.delete()
    messages.success(request, "File eliminato con successo")
    return redirect('advepa:file-manager')


@login_required(login_url='advepa:login')
def unlink_file_classroom(request, classroom_id, file_id):
    # Ottieni la classroom e il file
    classroom = get_object_or_404(Classroom, id=classroom_id)
    file = get_object_or_404(MediaFile, id=file_id)

    # Rimuovi il file dalla classroom
    classroom.media_files.remove(file)

    messages.success(request, "File rimosso con successo")
    return redirect('advepa:school-dashboard')


@login_required(login_url='advepa:login')
def delete_multiple_files(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = MediaFile.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Files eliminati con successo!'})
    response.status_code = 200
    return response
