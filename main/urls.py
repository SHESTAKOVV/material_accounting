from django.urls import path

from main import views


urlpatterns = [
    path('', views.home, name='home'),
    # path("register/", views.register, name="register"),
    path('logout/', views.logout_action, name='exit'),
    path("login/", views.custom_login, name="custom_login"),
    path("materials/", views.material_list, name="material_list"),
    path("materials/add/", views.material_create, name="material_add"),
    path("materials/<int:pk>/edit/", views.material_edit, name="material_edit"),
    path("materials/<int:pk>/delete/", views.material_delete, name="material_delete"),
]