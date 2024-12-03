from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logged_out.html'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='account/logged_out.html'), name='logged_out'),

    path('password-change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # url-адреса сброса пароля
    path('password-reset/',
    auth_views.PasswordResetView.as_view(),
    name='password_reset'),
    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(),
    name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'),
    path('password-reset/complete/',
    auth_views.PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),


    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
