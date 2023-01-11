from django.urls import path, reverse_lazy
from account.views import *
from django.contrib.auth import views

app_name = "account"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', user_logout, name='logout'),
    path('email_verification/<str:uidb64>/<str:token>', email_verification, name='email_verification'),
    path('email_verification_sent/', email_verification_sent, name='email_verification_sent'),
    path('email_verification_success/', email_verification_success, name='email_verification_success'),
    path('profile/', profile, name='profile'),
    path('delete/', delete_account, name='delete'),
    path('reset_password/', views.PasswordResetView.as_view(template_name='account/password/reset_password.html', success_url=reverse_lazy('account:password_reset_done'), email_template_name='account/password/reset_password_email.html'), name='reset_password'),
    path('reset_password_sent/', views.PasswordResetDoneView.as_view(template_name='account/password/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(template_name='account/password/reset.html', success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', views.PasswordResetCompleteView.as_view(template_name='account/password/reset_password_complete.html'), name='password_reset_complete'),
    path('manage_shipping/', manage_shipping, name='manage_shipping'),
]
