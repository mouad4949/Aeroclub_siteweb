
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile,Reservation, Service,avion
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime,timedelta
class CustomUserCreationForm(UserCreationForm):
    Prenom = forms.CharField(max_length=30, required=True, help_text='Required')
    Nom = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    tel = forms.CharField(max_length=15, required=True, help_text='Required')
    Nationalité = forms.CharField(max_length=50, required=True, help_text='Required')
    ville = forms.CharField(max_length=50, required=True, help_text='Required')
    Domicile = forms.CharField(max_length=50, required=True, help_text='Required')
    date_naissance = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    CIN = forms.CharField(max_length=15, required=True, help_text='Required')
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ( 
            'username',
            'email', 
            'password1', 
            'password2', 
            
        )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Vérifiez si un profil existe déjà pour cet utilisateur
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'tel': self.cleaned_data['tel'],
                    'Nationalité': self.cleaned_data['Nationalité'],
                    'Ville': self.cleaned_data['ville'],
                    'Domicile': self.cleaned_data['Domicile'],
                    'date_naissance': self.cleaned_data['date_naissance'],
                    'CIN': self.cleaned_data['CIN'],
                    'Nom': self.cleaned_data['Nom'],
                    'prenom': self.cleaned_data['Prenom'],
                    'age': self.cleaned_data['age']
                }
            )
            if not created:
                # Mettez à jour le profil existant si nécessaire
                profile.tel = self.cleaned_data['tel']
                profile.Nationalité = self.cleaned_data['Nationalité']
                profile.Ville = self.cleaned_data['ville']
                profile.Domicile = self.cleaned_data['Domicile']
                profile.date_naissance = self.cleaned_data['date_naissance']
                profile.CIN = self.cleaned_data['CIN']
                profile.Nom = self.cleaned_data['Nom']
                profile.prenom = self.cleaned_data['Prenom']
                profile.age = self.cleaned_data['age']
                profile.save()
        return user
User = get_user_model()




class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.',label='Email')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['type_reservation', 'av', 'date_depart', 'date_arrivé','payé_par_pack']
        widgets = {
            'date_depart': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_arrivé': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['type_reservation'].widget.attrs.update({'class': 'form-control', 'onchange': 'updatePrice()'})

        # Récupérer les avions disponibles
        available_avions = avion.objects.filter(Disponibilité=True)

        # Préparer les choix pour le champ av
        choix_de_place = [(av.id, f"{av.nom} - {av.Nombres_de_places} places") for av in available_avions]
        
        # Assigner les choix au champ av
        self.fields['av'].choices = choix_de_place

    def clean(self):
        cleaned_data = super().clean()
        date_depart = cleaned_data.get('date_depart')
        date_arrivé = cleaned_data.get('date_arrivé')
        av = cleaned_data.get('av')

        # Log pour vérifier les valeurs nettoyées
        print(f'Date de départ: {date_depart}, Date d\'arrivée: {date_arrivé}')

        if date_depart and date_arrivé:
            if date_arrivé <= date_depart:
                raise ValidationError("La date d'arrivée doit être après la date de départ.")

            # Calculer la durée
            duree = (date_arrivé - date_depart).total_seconds() / 3600*60  # en heures
            cleaned_data['duree'] = duree

            # Vérifier si l'avion est déjà réservé pendant cette période
            overlapping_reservations = Reservation.objects.filter(
                av=av,
                Status='validé',
                date_depart__lt=date_arrivé,
                date_arrivé__gt=date_depart
            ).exclude(id=self.instance.id)

            if overlapping_reservations.exists():
                raise ValidationError(
                    "Cet avion est déjà réservé pendant la période choisie. Veuillez sélectionner un autre avion ou modifier les horaires."
                )

        type_reservation = cleaned_data.get('type_reservation')

        if type_reservation:
            try:
                service = Service.objects.get(type_service=type_reservation)
                cleaned_data['prix'] = service.prix
            except Service.DoesNotExist:
                self.add_error('type_reservation', 'Invalid type of reservation')

        return cleaned_data



        
       