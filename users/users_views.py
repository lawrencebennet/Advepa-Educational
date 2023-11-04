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
from advepa.models import Action, Import, GraphInteraction
from django.shortcuts import render
from users.forms import UploadMediaFileForm


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
                if not check_school_setted(request):
                    return redirect('advepa:page-error-403')
                role = request.user.get_role_display()
                if request.user.is_superuser or request.user.role == 'advepa':
                    mex = "Benvenuto nella dashboard di amministrazione"
                elif role == "student":
                    messages.warning(request, "Non sei autorizzato ad entrare!")
                    return redirect('advepa:page-error-403')
                else:
                    mex = f'Benvenuto alla Dashboard per gli {role}'
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    if request.user.is_superuser or request.user.role == 'advepa':
                        messages.success(request, mex)
                        return redirect('advepa:dashboard')
                    elif role == "Nessun ruolo":
                        return redirect('advepa:page-error-403')
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
def advepa_dashboard(request):
    if request.user.role == 'advepa' or request.user.is_superuser:
        # INTERAZIONI
        last_day_graph_interactions = GraphInteraction.objects.filter(
            time__gt=datetime.now() - timedelta(hours=24)).count()

        # Numero di utenti che hanno effettuato il login dalle 24 alle 48 ore fa
        previous_day_interactions = GraphInteraction.objects.filter(time__gt=datetime.now() - timedelta(hours=48),
                                                                    time__lt=datetime.now() - timedelta(
                                                                        hours=24)).count()

        # Calcolo la differenza e la percentuale di aumento o diminuzione rispetto al giorno precedente
        diff = last_day_graph_interactions - previous_day_interactions
        percent_change_interactions = (
                                              diff / previous_day_interactions) * 100 if previous_day_interactions != 0 else 100
        if diff < 0:
            percent_change_interactions = f"-{percent_change_interactions}%"
        else:
            percent_change_interactions = f"+{percent_change_interactions}%"

        # UTENTI
        last_day_logins = CustomUser.objects.filter(last_login__gt=datetime.now() - timedelta(hours=24)).count()

        # Numero di utenti che hanno effettuato il login dalle 24 alle 48 ore fa
        previous_day_logins = CustomUser.objects.filter(last_login__gt=datetime.now() - timedelta(hours=48),
                                                        last_login__lt=datetime.now() - timedelta(hours=24)).count()

        # Calcolo la differenza e la percentuale di aumento o diminuzione rispetto al giorno precedente
        diff = last_day_logins - previous_day_logins
        percent_change_login = (diff / previous_day_logins) * 100 if previous_day_logins != 0 else 100
        if diff < 0:
            percent_change_logins = f"-{percent_change_login}%"
        else:
            percent_change_logins = f"+{percent_change_login}%"
        total_users = CustomUser.objects.count()
        # Ultimo utente creato
        # last_user = CustomUser.objects.order_by('-date_joined').first()
        # Calcola i giorni trascorsi dalla creazione dell'ultimo utente
        # days_since_last_user = (timezone.now() - last_user.date_joined).days
        days_since_last_user = 10
        user_list = list(CustomUser.objects.order_by('-last_login'))
        last_import = Import.objects.last()
        total_exhibitions = Exhibition.objects.count()
        total_actions = Action.objects.count()
        context = {
            "user_list": user_list,
            "last_import": last_import,
            "total_exhibitions": total_exhibitions,
            "total_actions": total_actions,
            'days_since_last_user': days_since_last_user,
            'total_users': total_users,
            'last_day_logins': last_day_logins,
            'percent_change_logins': percent_change_logins,
            'last_day_graph_interactions': last_day_graph_interactions,
            'percent_change_interactions': percent_change_interactions,
        }
        return render(request, "advepa/advepa_dashboard.html", context)
    else:
        return render(request, "403.html")


def calcolachart(start_date, finish_date, filters, chart_labels, chart_action_count, days, model):
    if days != 1:
        finish_date -= timedelta(days=1)
    while start_date <= finish_date:
        date_tmp = start_date + timedelta(days=days)
        if model == "Action":
            count = Action.objects.filter(filters & Q(date__gte=start_date, date__lte=date_tmp)).count()
        elif model == "Access":
            count = SiteLogins.objects.filter(filters & Q(date__gte=start_date, date__lte=date_tmp)).count()
        else:
            count = 0
        if days != 1:
            chart_labels.append(
                f"{start_date.strftime('%d-%m-%Y')} / {date_tmp.strftime('%d-%m-%Y')}")
        else:
            chart_labels.append(
                f"{start_date.strftime('%d-%m-%Y')}")
        chart_action_count.append(count)
        start_date = date_tmp
    return chart_labels, chart_action_count


# FIERE E GRAFICI
@login_required(login_url='advepa:login')
def actions_charts(request):
    # if check_stand_or_exhibition_setted(request):
    #     return redirect('advepa:page-error-403')
    disabled_exhibition = False
    disabled_stand = False
    exhibition_from_user = None
    stand_from_user = None
    disabled_exhibition_id = -1
    disabled_stand_id = -1
    if request.user.role == 'administrator':
        if request.user.exhibitions:
            exhibition_from_user = request.user.exhibitions
            disabled_exhibition = True
            disabled_exhibition_id = exhibition_from_user.id
    elif request.user.role == 'standist':
        if request.user.stands:
            stand_from_user = request.user.stands
            disabled_exhibition = True
            disabled_stand = True
            disabled_exhibition_id = stand_from_user.pavilion_set.first().exhibition_set.first().id
            disabled_stand_id = stand_from_user.id
    exhibition_list = list(Exhibition.objects.all())
    stand_list = list(Stand.objects.all())
    selected_exhibition = 'all'
    selected_stand = 'all'
    selected_platform = 'all'
    selected_date_interval = 'lastseven'
    selected_date_range = f'{datetime.today().strftime("%m-%d-%Y")} - {datetime.today().strftime("%m-%d-%Y")}'
    chart_labels = []
    chart_action_count = []
    selected_date_radio = 'interval'
    filters = Q()
    today = datetime.today().date()

    # per il widget in alto
    now = timezone.now()
    last_7_days = now - timedelta(days=7)
    last_24_hours = now - timedelta(hours=24)
    actions_last_7_days = Action.objects.filter(date__gte=last_7_days).count()
    if actions_last_7_days == 0:
        percentage_last_24_hours = 0
    else:
        num_last_24_hours = Action.objects.filter(date__gte=last_24_hours).count()
        percentage_last_24_hours = num_last_24_hours / actions_last_7_days * 100

    if request.method == 'POST':
        GraphInteraction.objects.create(
            **{'time': now})
        exhibition_filter_id = request.POST.get('exhibition-select')
        stand_filter_id = request.POST.get('stand-select')
        platform_filter_id = request.POST.get('platform-select')
        date_interval_filter_id = request.POST.get('date-interval-select')
        date_range_filter_id = request.POST.get('date-range')
        date_radio_filter_id = request.POST.get('date-radio')
        if exhibition_from_user:
            filters = filters & Q(exhibition=exhibition_from_user)
        elif exhibition_filter_id and exhibition_filter_id != 'all':
            selected_exhibition = int(exhibition_filter_id)
            filters = filters & Q(exhibition_id=exhibition_filter_id)
        if stand_from_user:
            filters = filters & Q(stand=stand_from_user)
        elif stand_filter_id and stand_filter_id != 'all':
            selected_stand = int(stand_filter_id)
            filters = filters & Q(stand_id=stand_filter_id)
        if platform_filter_id and platform_filter_id != 'all':
            selected_platform = platform_filter_id
            filters = filters & Q(platform=platform_filter_id)
        if date_interval_filter_id and date_interval_filter_id == 'all':
            # restituisce la data più vecchia
            oldest_date = Action.objects.aggregate(oldest_date=Min('date'))['oldest_date'].date()
            # restituisce la data più nuova
            newest_date = Action.objects.aggregate(newest_date=Max('date'))['newest_date'].date()
            chart_labels, chart_action_count = calcolachart(oldest_date, newest_date, filters,
                                                            chart_labels, chart_action_count,
                                                            1, "Actions")
            selected_date_interval = 'all'
        elif date_interval_filter_id and date_radio_filter_id == 'interval':
            selected_date_interval = date_interval_filter_id
            dict_interval = {'lastseven': 7,
                             'lastfourteen': 14,
                             'lastthirty': 30,
                             'lastninety': 90,
                             'lastyear': 365}
            interval = today - timedelta(days=dict_interval[selected_date_interval])
            if selected_date_interval == 'lastseven':
                days = 1
            elif selected_date_interval == 'lastfourteen':
                days = 2
            elif selected_date_interval == 'lastthirty':
                days = 5
            elif selected_date_interval == 'lastninety':
                days = 10
            elif selected_date_interval == 'lastyear':
                days = 73
            else:
                days = 1

            chart_labels, chart_action_count = calcolachart(interval, today, filters,
                                                            chart_labels, chart_action_count,
                                                            days, "Actions")
            filters = filters & Q(date__gte=interval, date__lte=today)
        if date_range_filter_id and date_radio_filter_id == 'range':
            selected_date_radio = 'range'
            list_date_range = date_range_filter_id.split(' - ')
            date_start_string = list_date_range[0]
            date_finish_string = list_date_range[1]
            date_start = datetime.strptime(date_start_string, "%m/%d/%Y")
            date_finish = datetime.strptime(date_finish_string, "%m/%d/%Y")
            formatted_start = date_start.strftime("%Y-%m-%d %H:%M")
            formatted_finish = date_finish.strftime("%Y-%m-%d %H:%M")
            selected_date_range = f'{date_start_string} - {date_finish_string}'
            filters = filters & Q(date__gte=formatted_start, date__lte=formatted_finish)
            chart_labels, chart_action_count = calcolachart(date_start, date_finish, filters,
                                                            chart_labels, chart_action_count,
                                                            1, "Actions")

        group_list = (
            Action.objects.filter(filters)
                .values('exhibition__name', 'pavilion__name', 'stand__name', 'main_action', 'action_detail')
                .annotate(quantity=Count('id'))
        )
    else:
        interval = today - timedelta(days=7)
        chart_labels, chart_action_count = calcolachart(interval, today, filters,
                                                        chart_labels, chart_action_count,
                                                        1, "Actions")
        group_list = (
            Action.objects.filter(date__gte=interval, date__lte=today)
                .values('exhibition__name', 'pavilion__name', 'stand__name', 'main_action', 'action_detail')
                .annotate(quantity=Count('id'))
        )

    group_actions_list = []
    for group in group_list:
        group_actions_list.append(
            {
                'exhibition': group['exhibition__name'],
                'pavilion': group['pavilion__name'],
                'stand': group['stand__name'],
                'main_action': group['main_action'],
                'action_detail': group['action_detail'],
                'quantity': group['quantity'],
            }
        )
    context = {
        "page_title": "Visualizzazione Dati",
        "exhibition_list": exhibition_list,
        "stand_list": stand_list,
        "group_actions": group_actions_list,
        'selected_exhibition': selected_exhibition,
        'selected_stand': selected_stand,
        'selected_platform': selected_platform,
        'selected_date_interval': selected_date_interval,
        'selected_date_range': selected_date_range,
        'selected_date_radio': selected_date_radio,
        'chart_labels': chart_labels,
        'chart_data': chart_action_count,
        'actions_last_7_days': actions_last_7_days,
        'percentage_last_24_hours': percentage_last_24_hours,
        'disabled_exhibition': disabled_exhibition,
        'disabled_stand': disabled_stand,
        'disabled_exhibition_id': disabled_exhibition_id,
        'disabled_stand_id': disabled_stand_id,
    }
    return render(request, "advepa/actions_charts.html", context)


@login_required(login_url='advepa:login')
def get_stands(request, exhibition_id):
    if exhibition_id == 'all':
        stands = list(Stand.objects.all())
    else:
        exhibition = Exhibition.objects.get(id=exhibition_id)
        stands = exhibition.pavilion_set.stand_set.all()
    stand_options = ""
    for stand in stands:
        stand_options += f"<option value='{stand.id}'>{stand.name}</option>"
    return JsonResponse({"stand_options": stand_options})


@login_required(login_url='advepa:login')
def access_charts(request):
    # if check_stand_or_exhibition_setted(request):
    #     return redirect('advepa:page-error-403')
    if request.user.role == 'administrator' or request.user.role == 'standist':
        return redirect('advepa:page-error-403')
    selected_user = 'all'
    selected_date_interval = 'lastseven'
    selected_date_range = f'{datetime.today().strftime("%m-%d-%Y")} - {datetime.today().strftime("%m-%d-%Y")}'
    chart_labels = []
    chart_action_count = []
    selected_date_radio = 'interval'
    filters = Q()
    today = datetime.today().date()
    # user_list = CustomUser.objects.exclude(is_superuser=True).order_by('username','email') #in caso vogliamo escludere il superuser etc..
    user_list = CustomUser.objects.all().order_by('username', 'email')

    # per il widget in alto
    now = timezone.now()
    last_7_days = now - timedelta(days=7)
    last_24_hours = now - timedelta(hours=24)
    actions_last_7_days = SiteLogins.objects.filter(date__gte=last_7_days).count()
    if actions_last_7_days == 0:
        percentage_last_24_hours = 0
    else:
        num_last_24_hours = SiteLogins.objects.filter(date__gte=last_24_hours).count()
        percentage_last_24_hours = num_last_24_hours / actions_last_7_days * 100

    if request.method == 'POST':
        GraphInteraction.objects.create(
            **{'time': now})
        user_filter_id = request.POST.get('user-select')
        date_interval_filter_id = request.POST.get('date-interval-select')
        date_range_filter_id = request.POST.get('date-range')
        date_radio_filter_id = request.POST.get('date-radio')
        if user_filter_id and user_filter_id != 'all':
            filters = filters & Q(user__id=user_filter_id)
            selected_user = user_filter_id
        if date_interval_filter_id and date_interval_filter_id == 'all':
            # restituisce la data più vecchia
            oldest_date = Action.objects.aggregate(oldest_date=Min('date'))['oldest_date'].date()
            # restituisce la data più nuova
            newest_date = Action.objects.aggregate(newest_date=Max('date'))['newest_date'].date()
            chart_labels, chart_action_count = calcolachart(oldest_date, newest_date, filters,
                                                            chart_labels, chart_action_count,
                                                            1, "Access")
            selected_date_interval = 'all'
        elif date_interval_filter_id and date_radio_filter_id == 'interval':
            selected_date_interval = date_interval_filter_id
            dict_interval = {'lastseven': 7,
                             'lastfourteen': 14,
                             'lastthirty': 30,
                             'lastninety': 90,
                             'lastyear': 365}
            interval = today - timedelta(days=dict_interval[selected_date_interval])
            if selected_date_interval == 'lastseven':
                days = 1
            elif selected_date_interval == 'lastfourteen':
                days = 2
            elif selected_date_interval == 'lastthirty':
                days = 5
            elif selected_date_interval == 'lastninety':
                days = 10
            elif selected_date_interval == 'lastyear':
                days = 73
            else:
                days = 1

            chart_labels, chart_action_count = calcolachart(interval, today, filters,
                                                            chart_labels, chart_action_count,
                                                            days, "Access")
            filters = filters & Q(date__gte=interval, date__lte=today)
        if date_range_filter_id and date_radio_filter_id == 'range':
            selected_date_radio = 'range'
            list_date_range = date_range_filter_id.split(' - ')
            date_start_string = list_date_range[0]
            date_finish_string = list_date_range[1]
            date_start = datetime.strptime(date_start_string, "%m/%d/%Y")
            date_finish = datetime.strptime(date_finish_string, "%m/%d/%Y")
            formatted_start = date_start.strftime("%Y-%m-%d %H:%M")
            formatted_finish = date_finish.strftime("%Y-%m-%d %H:%M")
            selected_date_range = f'{date_start_string} - {date_finish_string}'
            filters = filters & Q(date__gte=formatted_start, date__lte=formatted_finish)
            chart_labels, chart_action_count = calcolachart(date_start, date_finish, filters,
                                                            chart_labels, chart_action_count,
                                                            1, "Access")
    else:
        interval = today - timedelta(days=7)
        chart_labels, chart_action_count = calcolachart(interval, today, filters,
                                                        chart_labels, chart_action_count,
                                                        1, "Access")

    context = {
        "page_title": "Visualizzazione Dati",
        "user_list": user_list,
        "selected_user": selected_user,
        'selected_date_interval': selected_date_interval,
        'selected_date_range': selected_date_range,
        'selected_date_radio': selected_date_radio,
        'chart_labels': chart_labels,
        'chart_data': chart_action_count,
        'actions_last_7_days': actions_last_7_days,
        'percentage_last_24_hours': percentage_last_24_hours,
    }
    return render(request, "advepa/access_charts.html", context)


# EXHIBITIONS
@login_required(login_url='advepa:login')
@permission_required({'users.view_exhibitions'}, raise_exception=True)
def exhibitions(request):
    exhibition_list = Exhibition.objects.filter().order_by('name')

    paginator = Paginator(exhibition_list, 10)  # Show 10 Users per page.
    context = {
        "exhibition_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Fiere"
    }
    return render(request, "advepa/modules/exhibitions.html", context)


@login_required(login_url='advepa:login')
@permission_required({'users.view_exhibition', 'users.change_exhibition'}, raise_exception=True)
def edit_exhibition(request, id):
    exhibition_obj = get_object_or_404(Exhibition, id=id)
    if request.method == 'POST':
        form = EditExhibitionForm(request.POST, request.FILES, instance=exhibition_obj)
        if form.is_valid():
            exhibition_obj = form.save()
            exhibition_obj.pavilions.clear()
            for i in form.cleaned_data['pavilions']:
                exhibition_obj.pavilions.add(i)
            return redirect('advepa:exhibitions')
    else:
        form = EditExhibitionForm(instance=exhibition_obj)
    status = "Modifica"
    return render(request, 'advepa/modules/add-exhibition.html',
                  {'form': form, 'status': status, "page_title": "Modifica Fiera"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_exhibition', 'users.add_exhibition'}, raise_exception=True)
def add_exhibition(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        if form.is_valid():
            exhibition_obj = form.save()
            exhibition_obj.pavilions.clear()
            for i in form.cleaned_data.get('pavilions'):
                exhibition_obj.pavilions.add(i)
            messages.success(request, f'Fiera {exhibition_obj.name} creata con successo!')
            return redirect('advepa:exhibitions')
    else:
        form = ExhibitionForm()
    return render(request, 'advepa/modules/add-exhibition.html', {'form': form, "page_title": "Crea Fiera"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_exhibition', 'users.delete_exhibition'}, raise_exception=True)
def delete_exhibition(request, id):
    e = Exhibition.objects.get(id=id)
    e.delete()
    messages.success(request, "Exhibition deleted successfully")
    return redirect('advepa:exhibitions')


@login_required(login_url='advepa:login')
@permission_required({'users.view_exhibition', 'users.delete_exhibition'}, raise_exception=True)
def delete_multiple_exhibition(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = Exhibition.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Fiere eliminate con successo!'})
    response.status_code = 200
    return response


# PAVILIONS
@login_required(login_url='advepa:login')
@permission_required({'users.view_pavilions'}, raise_exception=True)
def pavilions(request):
    pavilion_list = Pavilion.objects.filter().order_by('name')

    paginator = Paginator(pavilion_list, 10)  # Show 10 Users per page.
    context = {
        "pavilion_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Padiglioni"
    }
    return render(request, "advepa/modules/pavilions.html", context)


@login_required(login_url='advepa:login')
@permission_required({'users.view_pavilion', 'users.change_pavilion'}, raise_exception=True)
def edit_pavilion(request, id):
    obj = get_object_or_404(Pavilion, id=id)
    if request.method == 'POST':
        form = EditPavilionForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            obj.stands.clear()
            for i in form.cleaned_data['stands']:
                obj.stands.add(i)
            return redirect('advepa:pavilions')
    else:
        form = EditPavilionForm(instance=obj)
    status = "Modifica"
    return render(request, 'advepa/modules/add-pavilion.html',
                  {'form': form, 'status': status, "page_title": "Modifica Padiglione"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_pavilion', 'users.add_pavilion'}, raise_exception=True)
def add_pavilion(request):
    if request.method == 'POST':
        form = PavilionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.stands.clear()
            for i in form.cleaned_data.get('stands'):
                obj.stands.add(i)
            messages.success(request, f'Padiglione {obj.name} creato con successo!')
            return redirect('advepa:pavilions')
    else:
        form = PavilionForm()
    return render(request, 'advepa/modules/add-pavilion.html', {'form': form, "page_title": "Crea Padiglione"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_pavilion', 'users.delete_pavilion'}, raise_exception=True)
def delete_pavilion(request, id):
    o = Pavilion.objects.get(id=id)
    o.delete()
    messages.success(request, "Pavilion deleted successfully")
    return redirect('advepa:pavilions')


@login_required(login_url='advepa:login')
@permission_required({'users.view_pavilion', 'users.delete_pavilion'}, raise_exception=True)
def delete_multiple_pavilion(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        obj = Pavilion.objects.get(pk=id)
        obj.delete()

    response = JsonResponse({"success": 'Padiglioni eliminati con successo!'})
    response.status_code = 200
    return response


# STANDS
@login_required(login_url='advepa:login')
@permission_required({'users.view_stands'}, raise_exception=True)
def stands(request):
    stand_list = Stand.objects.filter().order_by('name')

    paginator = Paginator(stand_list, 10)  # Show 10 Users per page.
    context = {
        "stand_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Stands"
    }
    return render(request, "advepa/modules/stands.html", context)


@login_required(login_url='advepa:login')
@permission_required({'users.view_stand', 'users.change_stand'}, raise_exception=True)
def edit_stand(request, id):
    obj = get_object_or_404(Stand, id=id)
    if request.method == 'POST':
        form = EditStandForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            return redirect('advepa:stands')
    else:
        form = EditStandForm(instance=obj)
    status = "Modifica"
    return render(request, 'advepa/modules/add-stand.html',
                  {'form': form, 'status': status, "page_title": "Modifica Stand"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_stand', 'users.add_stand'}, raise_exception=True)
def add_stand(request):
    if request.method == 'POST':
        form = StandForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Stand {obj.name} creato con successo!')
            return redirect('advepa:stands')
    else:
        form = StandForm()
    return render(request, 'advepa/modules/add-stand.html', {'form': form, "page_title": "Crea Stand"})


@login_required(login_url='advepa:login')
@permission_required({'users.view_stand', 'users.delete_stand'}, raise_exception=True)
def delete_stand(request, id):
    o = Stand.objects.get(id=id)
    o.delete()
    messages.success(request, "Stand deleted successfully")
    return redirect('advepa:stands')


@login_required(login_url='advepa:login')
@permission_required({'users.view_stand', 'users.delete_stand'}, raise_exception=True)
def delete_multiple_stand(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        obj = Stand.objects.get(pk=id)
        obj.delete()

    response = JsonResponse({"success": 'Stands eliminati con successo!'})
    response.status_code = 200
    return response


@login_required(login_url='advepa:login')
def import_actions(request):
    # if check_stand_or_exhibition_setted(request):
    #     return redirect('advepa:page-error-403')
    action_count = 0
    start_time = datetime.now()
    list_actions = []
    response = requests.get("https://www.vinophila.com/service/api/export/visits-noauth/")
    data = json.loads(response.text)
    try:
        for key in data:
            if key == 'response':
                continue
            action = data[key]
            exhibition = Exhibition.objects.get(name='Vinophila')
            pavilion_string = action['location']['pavilion']
            pavilion = Pavilion.objects.filter(Q(exhibition=exhibition) & Q(name=pavilion_string))
            if not pavilion:
                pavilion = Pavilion.objects.create(**{'name': pavilion_string})
                exhibition.pavilions.add(pavilion)
            else:
                pavilion = pavilion[0]
            stand_string = action['location']['spot']
            if stand_string == '':
                stand_string = 'Login'
            stand = Stand.objects.filter(Q(pavilion=pavilion) & Q(name=stand_string))
            if not stand:
                stand = Stand.objects.create(**{'name': stand_string})
                pavilion.stands.add(stand)
            else:
                stand = stand[0]
            list_actions.append({
                'date': action['data'],
                'user': action['user'],
                'exhibition': exhibition,
                'pavilion': pavilion,
                'stand': stand,
                'main_action': action['action']['main'],
                'action_detail': action['action']['detail'],
                'platform': action['platform'],
                'country': action['geo']['country'],
                'region': action['geo']['region'],
                'province': action['geo']['province'],
                'municipality': action['geo']['municipality'],
            })
            action_count += 1
        for record in list_actions:
            if Action.objects.filter(**record).exists():
                Action.objects.filter(**record).delete()
            Action.objects.create(**record)
        finish_time = datetime.now()
        Import.objects.create(
            **{'imported_actions': action_count, 'exhibitions_updated': "1", 'start_time': start_time,
               'finish_time': finish_time, 'status': 'success'})
        messages.success(request, "Importazione eseguita correttamente!")
    except:
        finish_time = datetime.now()
        Import.objects.create(
            **{'imported_actions': action_count, 'exhibitions_updated': "1", 'start_time': start_time,
               'finish_time': finish_time})
        messages.warning(request, "Attenzione! L'ultima importazione è fallita")
    return redirect(reverse('advepa:dashboard'))


# SCHOOL


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
    context = {
        "school": school,
        "classroom_list": classrooms,
        "uploaded_file_list": paginator.get_page(request.GET.get('page')) if paginator else None,
        "all_file_list": all_file_list,
        "page_title": "Dashboard Scuola",
        "faq_section_1": faq_section_1,
        "faq_section_2": faq_section_2,
        "faq_section_3": faq_section_3
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
