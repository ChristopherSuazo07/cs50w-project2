from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_product",views.add_product, name ="add_product"),
    path("product/<int:id>/",views.show_product, name ="product"),
    path("watchlist/",views.watchlist, name ="watchlist"),
    path("add_watchlist/<int:id>/",views.add_watchlist, name ="add_watchlist"),
    path("remove_watchlist/<int:id>/",views.remove_watchlist, name ="remove_watchlist"),
    path("categories",views.categories, name ="categories"),
    path("category/<int:id>",views.category, name ="category"),

    path("add_new_deals/<int:id>", views.add_newpricefor_product, name="deals"),
    path("finish/Offer/<int:id>/",views.finishOffer, name="offerclose")

]
