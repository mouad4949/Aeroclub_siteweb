from celery import shared_task
from django.utils import timezone
from .models import avion,Reservation,Pilotes_Instructeur,Pilotes_Licencié,Reservation
from django.core.mail import send_mail
from testt.settings import EMAIL_HOST_USER
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
            mail_subject="Validation de votre réservation"
            message = (
            f"Bonjour {reservation.profile.prenom} {reservation.profile.Nom},\n\n"
            f"Nous avons le plaisir de vous informer que votre réservation a été validée !\n\n"
            f"Voici les détails de votre réservation :\n"
            f"Type de réservation : {reservation.type_reservation}\n"
            f"Date et heure : {reservation.date}\n"
            f"Durée : {reservation.duree} minutes\n"
            f"Avion réservé : {reservation.av.nom}\n"
            f"Pilote instructeur : {reservation.pilote.pilote.membre.profile.prenom} {reservation.pilote.pilote.membre.profile.Nom}\n"
            f"Numéro de téléphone du pilote : {reservation.pilote.pilote.membre.profile.tel}\n\n"
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
    return email_log

