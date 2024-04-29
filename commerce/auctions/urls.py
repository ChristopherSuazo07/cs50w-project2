from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_product",views.add_product, name = "add_product"),
    path("product/<int:id>/",views.show_product, name = "product")

]
