from django.urls import path, re_path
from advepa import advepa_views
from users import users_views
from advepa.serializers import *

app_name = 'advepa'
handler404 = 'advepa.advepa_views.page_error_404'
handler500 = 'advepa.advepa_views.page_error_500'
urlpatterns = [

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

    # ERRORI
    path('page-error-400/', advepa_views.page_error_400, name="page-error-400"),
    path('page-error-403/', advepa_views.page_error_403, name="page-error-403"),
    path('page-error-404/', advepa_views.page_error_404, name="page-error-404"),
    path('page-error-500/', advepa_views.page_error_500, name="page-error-500"),
    path('page-error-503/', advepa_views.page_error_503, name="page-error-503"),

    # SCHOOL
    path('schools/', users_views.schools, name="schools"),
    path('school-details/<int:id>/', users_views.edit_school, name="school-details"),
    path('add-school/', users_views.add_school, name="add-school"),
    path('edit-school/<int:id>/', users_views.edit_school, name="edit-school"),
    path('delete-school/<int:id>/', users_views.delete_school, name="delete-school"),

    path('delete-multiple-school/', users_views.delete_multiple_school, name="delete-multiple-school"),
    path('school-dashboard/', users_views.school_dashboard, name="school-dashboard"),
    path('', users_views.school_dashboard, name="dashboard"),
    path('index/', advepa_views.index, name="index"),

    # FAQ
    path('add-faq/', users_views.add_faq, name="add-faq"),
    path('edit-faq/<int:id>/', users_views.edit_faq, name="edit-faq"),
    path('delete-faq/<int:id>/', users_views.delete_faq, name="delete-faq"),
    path('edit-faq-section/<int:id>/', users_views.edit_faq_section, name="edit-faq-section"),

    # BACHECA
    path('add-notice/<str:notice_type>/', users_views.add_notice, name="add-notice"),
    path('edit-notice/<int:id>/', users_views.edit_notice, name="edit-notice"),
    path('delete-notice/<int:id>/', users_views.delete_notice, name="delete-notice"),

    # MEDIAFILES
    path('file-manager/', users_views.file_manager, name="file-manager"),
    path('manager-delete-file/<int:file_id>/', users_views.delete_file, name="manager-delete-file"),
    path('unlink-file-classroom/<int:classroom_id>/<int:file_id>/', users_views.unlink_file_classroom,
         name="unlink-file-classroom"),
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
