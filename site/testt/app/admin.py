from django.contrib import admin
from .models import avion,New,Profile,Membre,Service,Reservation,Client,Pilotes_Instructeur,Pilotes_Licencié,Pilotes_Stagiare,Biens_Reservations,Pack
from .admin_forms import ReservationAdminForm
# Register your models here.
admin.site.register(avion)
admin.site.register(New)
admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Pilotes_Instructeur)
admin.site.register(Pilotes_Licencié)
admin.site.register(Pilotes_Stagiare)
admin.site.register(Biens_Reservations)
admin.site.register(Pack)

class MembreAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste
    list_display = ('profile', 'pack', 'date_abonnement', 'status', 'solde')

    # Liste des champs à rendre éditables dans le formulaire d'édition
    # Exclure 'solde' pour qu'il ne soit pas modifiable
    readonly_fields = ('solde',)

    # Personnalisation du formulaire d'administration
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Rendre le champ 'pack' et 'image' facultatif
        form.base_fields['pack'].required = False
        form.base_fields['image'].required = False
        return form
admin.site.register(Membre, MembreAdmin)

class ReservationAdmin(admin.ModelAdmin):
    form=ReservationAdminForm
    list_display = ['profile', 'type_reservation','date_de_reservation' ,'av', 'pilote', 'Status','date_depart','date_arrivé','paiement']
    list_filter = ['Status']
    search_fields = ['profile__user__username', 'type_reservation']
    actions = ['assign_available_pilot']
    ordering = ['date_de_reservation']  # Ordre croissant

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['pilote'].queryset = Pilotes_Instructeur.objects.filter(Disponibilité=True)
        # Supprimer date_de_reservation du formulaire d'édition
        if 'date_de_reservation' in form.base_fields:
            del form.base_fields['date_de_reservation']
        return form

    def assign_available_pilot(self, request, queryset):
        # Exemple d'action pour assigner automatiquement un pilote disponible
        for reservation in queryset:
            if reservation.pilote is None:
                available_pilots = Pilotes_Instructeur.objects.filter(Disponibilité=True)
                if available_pilots.exists():
                    reservation.pilote = available_pilots.first()
                    reservation.save()
        self.message_user(request, "Pilotes assignés aux réservations sélectionnées.")

    assign_available_pilot.short_description = "Assigner automatiquement un pilote disponible"

admin.site.register(Reservation, ReservationAdmin)


