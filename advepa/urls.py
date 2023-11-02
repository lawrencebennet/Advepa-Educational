from django.urls import path, re_path
from advepa import advepa_views
from users import users_views
from advepa.serializers import *

app_name = 'advepa'
handler404 = 'advepa.advepa_views.page_error_404'
handler500 = 'advepa.advepa_views.page_error_500'
urlpatterns = [

    path('access/', users_views.access_charts, name="access"),
    path('actions/', users_views.actions_charts, name="actions"),
    path('import-actions/', users_views.import_actions, name="import-actions"),

    path('login/', users_views.login_user, name="login"),
    path('logout/', users_views.logout_user, name="logout"),
    path('password/', users_views.change_password, name='change_password'),

    # UTENTE
    path('users/', users_views.users, name="users"),
    path('user-details/<int:id>/', users_views.user_details, name="user-details"),
    path('add-user/', users_views.add_user, name="add-user"),
    path('edit-user/<int:id>/', users_views.edit_user, name="edit-user"),
    path('delete-user/<int:id>/', users_views.delete_user, name="delete-user"),
    path('delete-multiple-user/', users_views.delete_multiple_user, name="delete-multiple-user"),
    path('groups/', users_views.groups_list, name="groups"),
    path('group-edit/<int:id>/', users_views.group_edit, name="group-edit"),
    path('group-delete/<int:id>/', users_views.group_delete, name="group-delete"),
    path('group-add/', users_views.group_add, name="group-add"),
    path('permissions/', users_views.permissions, name="permissions"),
    path('edit-permissions/<int:id>/', users_views.edit_permissions, name="edit-permissions"),
    path('delete-permissions/<int:id>/', users_views.delete_permissions, name="delete-permissions"),
    path('assign-permissions-to-user/<int:id>/', users_views.assign_permissions_to_user,
         name="assign-permissions-to-user"),
    # FIERA
    path('exhibitions/', users_views.exhibitions, name="exhibitions"),
    path('add-exhibition/', users_views.add_exhibition, name="add-exhibition"),
    path('edit-exhibition/<int:id>/', users_views.edit_exhibition, name="edit-exhibition"),
    path('delete-exhibition/<int:id>/', users_views.delete_exhibition, name="delete-exhibition"),
    path('delete-multiple-exhibition/', users_views.delete_multiple_exhibition, name="delete-multiple-exhibition"),

    # PADIGLIONI
    path('pavilions', users_views.pavilions, name="pavilions"),
    path('add-pavilion/', users_views.add_pavilion, name="add-pavilion"),
    path('edit-pavilion/<int:id>/', users_views.edit_pavilion, name="edit-pavilion"),
    path('delete-pavilion/<int:id>/', users_views.delete_pavilion, name="delete-pavilion"),
    path('delete-multiple-pavilion/', users_views.delete_multiple_pavilion, name="delete-multiple-pavilion"),

    # STANDS
    path('stands', users_views.stands, name="stands"),
    path('add-stand/', users_views.add_stand, name="add-stand"),
    path('edit-stand/<int:id>/', users_views.edit_stand, name="edit-stand"),
    path('delete-stand/<int:id>/', users_views.delete_stand, name="delete-stand"),
    path('delete-multiple-stand/', users_views.delete_multiple_stand, name="delete-multiple-stand"),

    # ERRORI
    path('page-error-400/', advepa_views.page_error_400, name="page-error-400"),
    path('page-error-403/', advepa_views.page_error_403, name="page-error-403"),
    path('page-error-404/', advepa_views.page_error_404, name="page-error-404"),
    path('page-error-500/', advepa_views.page_error_500, name="page-error-500"),
    path('page-error-503/', advepa_views.page_error_503, name="page-error-503"),

    # SCHOOOL DASHBOARD
    path('school-dashboard/', users_views.school_dashboard, name="school-dashboard"),
    path('', users_views.school_dashboard, name="dashboard"),
    # path('', users_views.advepa_dashboard, name="dashboard"),
    path('index/', advepa_views.index, name="index"),
    # MEDIAFILES
    path('file-manager/', users_views.file_manager, name="file-manager"),
    path('delete-file/<int:id>/', users_views.delete_file, name="delete-file"),
    path('unlink-file-classroom/<int:classroom_id>/<int:file_id>/', users_views.unlink_file_classroom, name="unlink-file-classroom"),
    path('delete-multiple-files/', users_views.delete_multiple_files, name="delete-multiple-files"),

    # API
    # path('api/school-details/', GetSchoolDetails.as_view(), name='school-details'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/user-change-avatar/', UserChangeAvatarView.as_view(), name='user-change-avatar'),
    path('api/media-files-classroom/', MediaFilesClassroom.as_view(), name='media-files-classroom'),
    path('api/faqs-school/', FaqsView.as_view(), name='faqs-school'),
    path('api/notices-school/', NoticesView.as_view(), name='notices-school'),

    re_path(r'^.*\.*', advepa_views.page_error_404, name='not-found'),
]
