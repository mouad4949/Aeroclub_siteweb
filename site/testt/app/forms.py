
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
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Reservation
        fields = ['type_reservation', 'date', 'av','duree']

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

    def clean_date(self):
        date = self.cleaned_data.get('date')

        # Convertir la date au fuseau horaire local si nécessaire
        date = localtime(date)

        # Vérifier s'il y a une réservation dans l'heure avant ou après la date sélectionnée
        delta = timedelta(hours=1)
        if Reservation.objects.filter(
            date__gte=date - delta,
            date__lte=date + delta,
            Status='validé',  # Ajoutez cette condition pour filtrer par statut
        ).exists():
            raise ValidationError("Il y a une autre réservation validée dans cette heure, veuillez choisir une autre horaire.")

        return date

    def clean(self):
        cleaned_data = super().clean()
        type_reservation = cleaned_data.get('type_reservation')

        if type_reservation:
            try:
                service = Service.objects.get(type_service=type_reservation)
                cleaned_data['prix'] = service.prix
            except Service.DoesNotExist:
                self.add_error('type_reservation', 'Invalid type of reservation')

        return cleaned_data

        
       