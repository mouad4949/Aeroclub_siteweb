from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import New,avion,Pilotes_Instructeur,Reservation
from .forms import CustomUserCreationForm,EmailAuthenticationForm,ReservationForm
from django.contrib.auth.models import User
from .tasks import check_avion_disponibility,send_mail_reservation
from django.http.response import HttpResponse
from django.utils.dateparse import parse_datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils.timezone import localtime

def index(request):
    actualité=New.objects.order_by("-id")
    av=avion.objects.order_by("-id")
    avions_count=avion.objects.count()
    pilote=Pilotes_Instructeur.objects.order_by("id")
    pilotes_count=pilote.count()
    context={"actualité":actualité,"av":av,"prof":pilote,"avions_count":avions_count,"pilotes_count":pilotes_count}
    return render(request,"app/index.html",context)

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Rediriger vers la page d'accueil après une connexion réussie
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Formulaire n\'est pas valide')
            print(form.errors)  # Pour le débogage
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')  # Assurez-vous que 'login' est bien le nom de votre vue de connexion

def Register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Rediriger vers la page de connexion après l'inscription réussie
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {'form': form})


def reserver_view(request):
    pr = 0
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.profile = request.user.profile
            reservation.prix = form.cleaned_data['prix']
            reservation.av=form.cleaned_data['av']
            reservation.Nbrs_places = reservation.av.Nombres_de_places
            reservation.save()
            messages.success(request, 'Reservation successful')
            return redirect('reserver')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = ReservationForm()
    # Récupérer toutes les dates et heures déjà réservées
    reserved_dates = list(Reservation.objects.filter(Status='validé').values_list('date', flat=True))

    # Convertir en JSON
    reserved_dates = json.dumps([date.isoformat() for date in reserved_dates], cls=DjangoJSONEncoder) 
    return render(request, 'app/reserver.html', {'form': form, 'pr': pr, 'reserved_dates': reserved_dates})



def send_mail(request):
    send_mail_reservation.delay()
    return HttpResponse("Sent")