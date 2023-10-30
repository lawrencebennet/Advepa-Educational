from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
# from users.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from django.urls import path
from users import users_views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('advepa.urls', namespace='advepa')),

    # path('reset_password/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
    #      name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/', users_views.change_password, name='change_password'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = "Advepa Dashboard"
admin.site.site_title = "Dashboard"
admin.site.index_title = "Dashboard"
