from django.urls import path
from . import views
from .views import login_view , logout_view,Register_view,reserver_view,send_mail

urlpatterns = [
    path("test/", send_mail ,name="mail"),
    path("index/", views.index, name="index"),
    path('login/', login_view, name='login'),
    path('register/', Register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('reserver/', reserver_view, name='reserver'),
]