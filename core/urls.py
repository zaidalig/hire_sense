from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path("", views.home_view, name="home"),  
    path("register/", views.register_view, name="register"),
    path('profile/', views.update_profile, name='update_profile'),
    path('profile/', views.update_profile, name='profile'),  # Profile view
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),  # protected view
    path("upload-resume/", views.upload_resume_view, name="upload_resume"),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
