from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path("", views.home_view, name="home"),  # 👈 Main landing page
    path("register/", views.register_view, name="register"),
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),  # protected view
    path("upload-resume/", views.upload_resume_view, name="upload_resume"),
]
