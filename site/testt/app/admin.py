from django.contrib import admin
from .models import avion,New,Profile,Membre,Service,Reservation,Client,Pilotes_Instructeur,Pilotes_Licencié,Pilotes_Stagiare
from .admin_forms import ReservationAdminForm
# Register your models here.
admin.site.register(avion)
admin.site.register(New)
admin.site.register(Profile)
admin.site.register(Membre)
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Pilotes_Instructeur)
admin.site.register(Pilotes_Licencié)
admin.site.register(Pilotes_Stagiare)

class ReservationAdmin(admin.ModelAdmin):
    form=ReservationAdminForm
    list_display = ['profile', 'type_reservation', 'date','date_de_reservation' ,'av', 'pilote', 'Status']
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

