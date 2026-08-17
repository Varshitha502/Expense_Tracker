from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_transaction, name="add_transaction"),
    path("edit/<int:id>/", views.edit_transaction, name="edit_transaction"),
    path("delete/<int:id>/", views.delete_transaction, name="delete_transaction"),
]
