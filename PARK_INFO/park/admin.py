from django.contrib import admin

# Register your models here.


from .models import *

class AdminEquipment(admin.ModelAdmin):
    list_display = ('serial_number', 'type_eq', 'brand', 'modele_eq', 'purchase_date', 'warranty_expire', 'status')

admin.site.register(Equipment, AdminEquipment)

admin.site.register(Maintenance)
admin.site.register(Region)
admin.site.register(EtatCivil)
admin.site.register(Commissariat)
admin.site.register(Prefecture)
admin.site.register(TypeEquipement)
admin.site.register(Direction)