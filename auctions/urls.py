from django.urls import path

from . import views

app_name = "commerce"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("delete", views.delete, name="delete"),
    path("<int:page_id>", views.listingpage, name="listingpage"),
    path("wish", views.wish, name="wish"),
    path("bidfunc", views.bidfunc, name="bidfunc"),
    path("invalidbidfunc", views.invalidbidfunc, name="invalidbidfunc"),
    path("closedbids", views.closedbids, name="closedbids"),
    path("commentsfunc", views.commentsfunc, name="commentsfunc"),
    path("listingall", views.listingall, name="listingall"),
    path("reply", views.reply, name="reply"),
    path("<str:category_name>", views.category, name="category")
]
