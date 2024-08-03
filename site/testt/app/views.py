from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import New,avion,Pilotes_Instructeur,Reservation,Profile,Membre,Pack,Biens_Reservations
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
import paypalrestsdk
import logging
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from django.templatetags.static import static
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
                return redirect('app:index')  # Rediriger vers la page d'accueil après une connexion réussie
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
    return redirect('app:index')  # Assurez-vous que 'login' est bien le nom de votre vue de connexion

def Register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('app:login')  # Rediriger vers la page de connexion après l'inscription réussie
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



@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    membre = Membre.objects.get(profile=profile)
    reservation = Reservation.objects.filter(profile=profile)  # Utilisation de filter pour obtenir toutes les réservations
    packs = Pack.objects.all()
    return render(request, 'app/profile.html', {
        'profile': profile,
        'membre': membre,
        'packs':packs,
        'reservation':reservation
    })



@login_required
def checkout(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    context = {
        'reservation': reservation,
    }
    return render(request, 'app/checkout.html', context)


@csrf_exempt
def payment_success(request, reservation_id):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        payer_id = request.POST.get('payerID')
        transaction_details = request.POST.get('transactionDetails')

        try:
            transaction_details = json.loads(transaction_details)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid transaction details'}, status=400)

        # Obtenez la réservation et créez ou mettez à jour Biens_Reservations
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.paiement = "payé"
        reservation.save()

        # Créez ou mettez à jour l'entrée dans Biens_Reservations
        bien, created = Biens_Reservations.objects.get_or_create(reservation=reservation)
        bien.type_paiement = "en ligne"
        bien.libellé = f"""
            transaction_id: {order_id}
            transaction_date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            montant_payé: {reservation.prix}
            service_paiement: PayPal
            email_paiement: {transaction_details.get('payer', {}).get('email_address', 'N/A')}
        """
        bien.save()

        # Redirection vers le template success.html
        return render(request, 'app/success.html', {'reservation_id': reservation_id})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



def payment_cancel(request, reservation_id):
    return render(request, 'app/cancel.html')





def generate_pdf(request, reservation_id):
    # Récupérer les détails de la réservation
    reservation = Reservation.objects.get(id=reservation_id)
    bien = Biens_Reservations.objects.get(reservation=reservation)

    # Chemin relatif de l'image dans le répertoire static
    image_path = settings.BASE_DIR / 'app' / 'static' / 'images' / 'pdf.png'

    # Créer un buffer pour stocker le PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Définir les dimensions de l'image (plus large que haute)
    image_width = width * 0.8  # Largeur de l'image à 80% de la largeur de la page
    image_height = image_width * 0.5  # Hauteur proportionnelle (50% de la largeur)

    # Ajouter l'image en tant que fond
    image_x = (width - image_width) / 2  # Centrer horizontalement
    image_y = (height - image_height) / 2  # Centrer verticalement
    c.drawImage(str(image_path), image_x, image_y, width=image_width, height=image_height, mask='auto')

    # Définir les styles de texte
    c.setFont('Helvetica-Bold', 16)
    
    # Centrer le titre au-dessus de l'image
    title = "Reçu de Paiement"
    title_width = c.stringWidth(title, 'Helvetica-Bold', 16)
    c.drawString((width - title_width) / 2, height - 50, title)

    # Infos Client
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 100, "Informations du Client")
    c.setFont('Helvetica', 10)
    c.drawString(100, height - 120, f"Nom : {reservation.profile.Nom}")
    c.drawString(100, height - 140, f"Prénom : {reservation.profile.prenom}")

    # Infos Réservation
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 180, "Détails de la Réservation")
    c.setFont('Helvetica', 10)
    c.drawString(100, height - 200, f"Type de réservation : {reservation.type_reservation}")
    c.drawString(100, height - 220, f"Prix : {reservation.prix} MAD")
    c.drawString(100, height - 240, f"Date de départ : {reservation.date_depart.strftime('%d/%m/%Y')}")
    c.drawString(100, height - 260, f"Date d'arrivée : {reservation.date_arrivé.strftime('%d/%m/%Y')}")
    c.drawString(100, height - 280, f"Durée : {reservation.duree} Minutes")
    c.drawString(100, height - 300, f"Avion : {reservation.av.nom}")
    c.drawString(100, height - 320, f"Nombres de places : {reservation.Nbrs_places} Place(s)")
    
    # Infos Pilote
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 360, "Détails du Pilote")
    c.setFont('Helvetica', 10)
    c.drawString(100, height - 380, f"Pilote : {reservation.pilote.pilote.membre.profile.Nom}, {reservation.pilote.pilote.membre.profile.prenom}")
    c.drawString(100, height - 400, f"Numéro de pilote : {reservation.pilote.pilote.membre.profile.tel}")

    # Infos Paiement
    c.setFont('Helvetica-Bold', 12)
    y_position = height - 440
    c.drawString(100, y_position, "Informations de Paiement")
    
    # Séparer les informations de paiement avec des lignes
    c.setFont('Helvetica', 10)
    y_position -= 20
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(100, y_position, width - 100, y_position)

    # Afficher les informations de paiement ligne par ligne
    if bien.libellé:
        for line in bien.libellé.splitlines():
            y_position -= 20
            c.drawString(100, y_position, line)
    else:
        y_position -= 20
        c.drawString(100, y_position, "Aucune information de paiement disponible.")

    # Ajouter le paragraphe de remerciement
    c.setFont('Helvetica', 10)
    y_position -= 40
    c.drawString(100, y_position, "Merci pour votre réservation. Nous espérons vous voir bientôt au Royal Aeroclub de Casablanca.")

    # Finaliser le PDF
    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recu_paiement_{reservation_id}.pdf"'
    return response

def send_mail(request):
    send_mail_reservation.delay()
    return HttpResponse("Sent")

