from celery import shared_task
from django.utils import timezone
from .models import avion,Reservation,Pilotes_Instructeur,Pilotes_Licencié,Reservation,Membre
from django.core.mail import send_mail
from testt.settings import EMAIL_HOST_USER
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings
@shared_task
def check_avion_disponibility():
    today = timezone.now().date()    
    avions = avion.objects.all()
    for av in avions:
        if av.CDN <= today or av.Licence_radio <= today or av.Assurance <= today :
            av.Disponibilité = False
        else:
            av.Disponibilité = True
        av.save()

@shared_task
def check_pilotes_disponibilty():
    today = timezone.now().date()
    pilotes=Pilotes_Instructeur.objects.all()
    for pil in pilotes:
        if pil.pilote.Carte_validité <=today:
            pil.Disponibilité=False
        else:
            pil.Disponibilité=True
        pil.save()

@shared_task(bind=True)
def send_mail_reservation(self):
    reservations=Reservation.objects.filter(Status="Validé", Sent=False)
    email_log = []
    for reservation in reservations:
        if reservation.payé_par_pack:
            mail_subject="Validation de votre réservation"
            date_depart_adjusted = reservation.date_depart + timedelta(hours=1)
            mem=Membre.objects.get(profile=reservation.profile)
            message = (
                f"Bonjour {reservation.profile.prenom} {reservation.profile.Nom},\n\n"
                f"Nous avons le plaisir de vous informer que votre réservation a été validée !\n\n"
                f"Voici les détails de votre réservation :\n"
                f"Type de réservation : {reservation.type_reservation}\n"
                f"Date et heure de départ : {date_depart_adjusted}\n"  # Utiliser la date ajustée
                f"Durée : {reservation.duree} minutes\n"
                f"Avion réservé : {reservation.av.nom}\n"
                f"Pilote instructeur : {reservation.pilote.pilote.membre.profile.prenom} {reservation.pilote.pilote.membre.profile.Nom}\n"
                f"Numéro de téléphone du pilote : {reservation.pilote.pilote.membre.profile.tel}\n\n"
                f"votre reservation est payé par votre pack .\n\n"
                f"Votre solde du votre pack restant : {mem.solde} minutes\n\n"
                f"Veuillez vous présenter au moins 45 minutes avant le vol.\n\n"
                f"Nous vous souhaitons un excellent vol !\n\n"
                f"Cordialement,\n"
                f"L'équipe de l'aéroclub"
            )
            to_email = reservation.profile.user.email
            from_email=EMAIL_HOST_USER
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True
            )
            reservation.Sent = True
            reservation.save()
            email_log.append({'from_email': from_email, 'to_email': to_email})
        else:
            mail_subject="Validation de votre réservation"
            date_depart_adjusted = reservation.date_depart + timedelta(hours=1)
            message_html = (
            f"<p>Bonjour {reservation.profile.prenom} {reservation.profile.Nom},</p>"
            f"<p>Nous avons le plaisir de vous informer que votre réservation a été validée !</p>"
            f"<p>Voici les détails de votre réservation :</p>"
            f"<ul>"
            f"    <li>Type de réservation : {reservation.type_reservation}</li>"
            f"    <li>Date et heure de départ : {date_depart_adjusted}</li>"
            f"    <li>Durée : {reservation.duree} minutes</li>"
            f"    <li>Avion réservé : {reservation.av.nom}</li>"
            f"    <li>Pilote instructeur : {reservation.pilote.pilote.membre.profile.prenom} {reservation.pilote.pilote.membre.profile.Nom}</li>"
            f"    <li>Numéro de téléphone du pilote : {reservation.pilote.pilote.membre.profile.tel}</li>"
            f"</ul>"
            f"<p>Veuillez vous présenter au moins 45 minutes avant le vol.</p>"
            f"<p>Vous pouver payer en ligne ou annuler votre reservation en cliquant sur le lien suivant:</p>"
            f"<p><a href='{'http://localhost:8000'}/app/login_mail'>Consulter votre réservation</a></p>"
            f"<p>Nous vous souhaitons un excellent vol !</p>"
            f"<p>Cordialement,<br>L'équipe de l'aéroclub</p>"
        )
            
        to_email = reservation.profile.user.email
        from_email = EMAIL_HOST_USER

        email = EmailMessage(
            subject=mail_subject,
            body=message_html,
            from_email=from_email,
            to=[to_email]
        )
        email.content_subtype = "html"  # Important pour envoyer un email en HTML
        email.send()

        reservation.Sent = True
        reservation.save()
        email_log.append({'from_email': from_email, 'to_email': to_email})
    return email_log


