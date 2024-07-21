from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Pilotes_Instructeur

class ReservationAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        av = cleaned_data.get('av')
        status = cleaned_data.get('Status')

        if status == 'validé':
            conflicting_reservations = Reservation.objects.filter(
                date=date,
                Status='validé'
            ).exclude(id=self.instance.id)

            if conflicting_reservations.exists():
                raise ValidationError(
                    "Il y a déjà une réservation validée pour cette date . Veuillez choisir une autre date ou un autre avion."
                )

        return cleaned_data
