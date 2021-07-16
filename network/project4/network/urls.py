from django.urls import path

from . import views

urlpatterns = [
    path("<int:page_number>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:user>/<int:page_number>", views.profile, name="profile"),
    path("following/<int:page_number>", views.following, name="following"),
    path("follow/<str:user>", views.follow, name="follow"),
    
    # API Routes
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like")
]
