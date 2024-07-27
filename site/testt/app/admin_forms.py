from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Pilotes_Instructeur,Membre

class ReservationAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        date_arrivé = cleaned_data.get('date_arrivé')
        date_depart = cleaned_data.get('date_depart')
        av = cleaned_data.get('av')
        status = cleaned_data.get('Status')

        if status == 'validé' and date_depart and date_arrivé:
            # Vérifier les conflits de réservation
            conflicting_reservations = Reservation.objects.filter(
                av=av,
                Status='validé',
                date_depart__lt=date_arrivé,
                date_arrivé__gt=date_depart
            ).exclude(id=self.instance.id)

            if conflicting_reservations.exists():
                raise ValidationError(
                    "Il y a déjà une réservation validée pour cet avion pendant la période choisie. Veuillez sélectionner une autre date ou un autre avion."
                )

        return cleaned_data
    



