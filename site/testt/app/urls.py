from django.urls import path,include
from . import views
from .views import login_view , logout_view,Register_view,reserver_view,send_mail,profile,generate_pdf,login_mail
app_name = 'app'
urlpatterns = [
    path("test/", send_mail ,name="mail"),
    path("index/", views.index, name="index"),
    path('login/', login_view, name='login'),
    path('register/', Register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('reserver/', reserver_view, name='reserver'),
    path('profile/',profile,name='profile'),
    path('paypal/',include('paypal.standard.ipn.urls')),
    path('checkout/<int:reservation_id>/', views.checkout, name='checkout'),
    path('success/<int:reservation_id>/', views.payment_success, name='success'),
    path('cancel/<int:reservation_id>/', views.payment_cancel, name='cancel'),
    path('download-receipt/<int:reservation_id>/', generate_pdf, name='download_receipt'),
    path('login_mail/', login_mail, name='login_email'),
]