from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import New,avion,Pilotes_Instructeur,Reservation,Profile,Membre
from .forms import CustomUserCreationForm,EmailAuthenticationForm,ReservationForm
from django.contrib.auth.models import User
from .tasks import check_avion_disponibility,send_mail_reservation
from django.http.response import HttpResponse
from django.utils.dateparse import parse_datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils.timezone import localtime,make_aware
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def process_date(date):
    if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
        aware_date = make_aware(date)
    else:
        aware_date = date
    return aware_date

def index(request):
    actualité = New.objects.order_by("-id")
    av = avion.objects.order_by("-id")
    avions_count = avion.objects.count()
    pilote = Pilotes_Instructeur.objects.order_by("id")
    pilotes_count = pilote.count()

    # Vérifier si l'utilisateur est authentifié
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Aucun profil associé

    context = {
        "actualité": actualité,
        "av": av,
        "prof": pilote,
        "avions_count": avions_count,
        "pilotes_count": pilotes_count,
        "profile": profile,  # Le profil peut être None pour les utilisateurs non connectés
    }
    return render(request, "app/index.html", context)

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


@login_required
def reserver_view(request):
    profile = Profile.objects.get(user=request.user)
    try:
        membre = Membre.objects.get(profile=profile)
    except Membre.DoesNotExist:
        membre = None

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Vérifiez et ajustez la date d'arrivée
            date_arrivé = form.cleaned_data.get('date_arrivé')
            if date_arrivé and (date_arrivé.tzinfo is None or date_arrivé.tzinfo.utcoffset(date_arrivé) is None):
                date_arrivé = timezone.make_aware(date_arrivé)

            reservation.date_arrivé = date_arrivé
            reservation.profile = request.user.profile
            reservation.prix = form.cleaned_data['prix']
            reservation.av = form.cleaned_data['av']
            reservation.Nbrs_places = reservation.av.Nombres_de_places
            reservation.duree = form.cleaned_data['duree']

            # Vérifiez si le membre a un solde suffisant
            if reservation.payé_par_pack:
                if membre and membre.solde >= reservation.duree:
                    reservation.paiement = 'payé'  # Marquer comme payé
                    
                    reservation.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error_message': "Votre solde est insuffisant pour effectuer cette réservation."
                    })
            else:
                reservation.save()  # Sauvegarder pour les autres méthodes de paiement
                return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False,
                'error_message': form.errors.as_text()  # Convertit les erreurs en texte pour l'affichage
            })
    else:
        form = ReservationForm()

    # Logique pour les dates réservées
    all_reserved_dates = Reservation.objects.filter(Status='validé')
    reserved_dates_by_avion = {
        avion.id: [
            {
                'start': reservation.date_depart.isoformat(),
                'end': reservation.date_arrivé.isoformat()
            }
            for reservation in all_reserved_dates if reservation.av.id == avion.id
        ] for avion in avion.objects.all()
    }
    reserved_dates_json = json.dumps(reserved_dates_by_avion, cls=DjangoJSONEncoder)

    return render(request, 'app/reserver.html', {
        'form': form,
        'reserved_dates': reserved_dates_json,
        'profile': profile,
        'membre': membre
    })





def send_mail(request):
    send_mail_reservation.delay()
    return HttpResponse("Sent")

