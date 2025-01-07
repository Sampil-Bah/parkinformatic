from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.db.models import Count

from itertools import chain

from authentification.models import User

from .models import *
from .utils import pagination


class HomeView(LoginRequiredMixin, View):
    
    template_name = 'park/list-equipments.html' 

    equipments  =  Equipment.objects.all()

    context = {
            'equipments': equipments,
    }

    def get(self,request, *args, **kwargs):        
        
        items = pagination(request, self.equipments)

        self.context['equipments'] = items

        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):

        equipment_id = request.GET.get('id')
        new_status = request.POST.get('status')
        
        # print(f'equipID:{equipment_id}')
        # print(f'statut:{new_status}')

        # Fetch the equipment object
        equipment = get_object_or_404(Equipment, id=equipment_id)
        
        # Update the status
        if equipment:
            equipment.status = new_status
            equipment.save()
            messages.success(request, 'statut changed successfully')  
            return JsonResponse({'success': True, 'new_status': new_status})

        equipments  =  Equipment.objects.all()

        context = {
            'equipments':equipments,
        }
            
        return render(request, self.template_name, context)
        
   
    
class EquipementView(LoginRequiredMixin, View):

    template_name = 'park/index.html'

    def get(self, request, *args, **kwargs):

        context = {
            'type_equipment' : TypeEquipement.objects.all(),
            'commissariats' : Commissariat.objects.all(),
            'etat_civils' : EtatCivil.objects.all(),
            'direction' : Direction.objects.all(),
        }

        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        try:

            numero_serie        = request.POST.get('numero_serie')
            type_equipment      = request.POST.get('type_equipment')
            marque              = request.POST.get('marque')
            modele              = request.POST.get('modele')
            date_achat          = request.POST.get('date_achat')
            guarantie           = request.POST.get('guarantie')
            statut              = request.POST.get('status')
            commissariat        = request.POST.get('commissariat')
            etat_civil          = request.POST.get('etat_civil')
            autres              = request.POST.get('autres')

            if commissariat:

                #print(f'commissariat:{commissariat}')

                equipment_object = {
                    'serial_number':numero_serie,        
                    'type_eq': TypeEquipement.objects.get(id=type_equipment),      
                    'brand': marque,              
                    'modele_eq': modele,              
                    'purchase_date':date_achat,          
                    'warranty_expire':guarantie,          
                    'status':statut,  
                    'commissariat' : Commissariat.objects.get(id=commissariat),
                }

            if etat_civil:

                #print(f'etat_civil:{etat_civil}')

                equipment_object = {
                    'serial_number':numero_serie,        
                    'type_eq': TypeEquipement.objects.get(id=type_equipment),      
                    'brand': marque,              
                    'modele_eq': modele,              
                    'purchase_date':date_achat,          
                    'warranty_expire':guarantie,          
                    'status':statut,  
                    'etat_civil': EtatCivil.objects.get(id=etat_civil),            
                }
            
            if autres:

                equipment_object = {
                    'serial_number':numero_serie,        
                    'type_eq': TypeEquipement.objects.get(id=type_equipment),      
                    'brand': marque,              
                    'modele_eq': modele,              
                    'purchase_date':date_achat,          
                    'warranty_expire':guarantie,          
                    'status':statut,  
                    'direction': Direction.objects.get(id=autres),            
                }
                

            created = Equipment.objects.create(**equipment_object)
            # print(f'created ...{created}')

            if created:
                messages.success(request, f'Equipement crée avec succes')
                return redirect('park:home')

            else:
                messages.error(request, f'Les données sont corrompues veuillez reessayez')

        except Exception as e :
            messages.error(request, f"Probleme d'enregistrement avec:{e}") 


        return render(self.request, self.template_name, {})
    


class MaintenanceView(LoginRequiredMixin, View):

    template_name = "park/maintenance.html"

    def get(self, request, *args, **kwargs):

        equipements = Equipment.objects.filter(status='panne')

        context = {
            'equipements': equipements,
        }

        return render(self.request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):

        try:
            equipment       = request.POST.get('equipment')
            technicien      = request.user
            issue_desc      = request.POST.get('probleme')
            action_taken    = request.POST.get('action')
            
            equipment = Equipment.objects.get(id=equipment)

            maintenance_obj = {
               'equipment' : equipment,      
               'technician' : technicien,      
               'issue_description' : issue_desc,      
               'action_taken' : action_taken,    
            }
            
            created = Maintenance.objects.create(**maintenance_obj)
            if created:
                messages.success(request, f'maintenance effectué avec succes')
                return redirect('park:home')
            else:
                messages.error(request, f'un probleme lors de lenregistrement des donnes')

        except Exception as e:
            messages.error(request, f"the following exception occured {e}")

        return render(self.request, self.template_name)
    

class AuditView(LoginRequiredMixin, View):

    template_name = 'park/audit.html'

    maintenance = Maintenance.objects.all()

    context = {
            'maintenance' : maintenance,
    }

    def get(self, request,  *args, **kwargs):

        items = pagination(request, self.maintenance)

        self.context['maintenance'] = items

        return render(request, self.template_name, self.context)


def get_detail_modal(request):

    object_id = request.GET.get('id') 

    if not object_id:
        print(f'object not found')
        return JsonResponse({'error': 'No equipment ID provided'}, status=400)

    try:

        obj = get_object_or_404(Equipment, id=object_id)  # Fetch the object from the database

    except Equipment.DoesNotExist:

        return JsonResponse({'error': 'Equipment not found'}, status=404)

    
   
    data = {
        'id': obj.id,
        'serial_number': obj.serial_number,  
        'type_eq': obj.type_eq.nom_equipement, 
        'brand': obj.brand,  
        'modele_eq': obj.modele_eq,  
        'purchase_date': obj.purchase_date.strftime('%Y-%m-%d'),  
        'warranty_expire': obj.warranty_expire.strftime('%Y-%m-%d'),
        'status': obj.status,  
    }

    # print(f'data:{data}')
    
    return JsonResponse(data)



class EquipmentAjaxSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query').strip().upper()
        print(f"query:{query}")
        query_upper = query.upper()
        query_lower = query.lower()
        if query:
           equipment = Equipment.objects.filter(
               models.Q(serial_number__iexact=query_upper) |
               models.Q(serial_number__iexact=query_lower)
            )
           #print(f'equipment:{equipment}')
        else:
            equipment = Equipment.objects.all()

        return render(request, 'park/search_results.html', {'equipments': equipment})

    
class EquipmentMaintenanceSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        query = request.GET.get('query', '').strip().upper()

        query_upper = query.upper()
        query_lower = query.lower()

        # print(f"query: {query}")

        # Fetch equipment from the Maintenance table based on the search query
        if query:
            maintenance = Maintenance.objects.filter(
            models.Q(equipment__serial_number__iexact=query_upper) |
            models.Q(equipment__serial_number__iexact=query_lower) |
            models.Q(technician__username__iexact=query_lower)
        )
        else:
            maintenance = Maintenance.objects.all()

        return render(request, 'park/audit_search.html', {'maintenance': maintenance})

    

class LocationsView(LoginRequiredMixin, View):

    template_name = 'park/location_.html'

    context = {
            'commissariats' : Commissariat.objects.all(),
            'etat_civils' : EtatCivil.objects.all(),
        }

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):

        commissariat_id = request.POST.get('commissariat')
        etat_civil_id = request.POST.get('etat_civil')
        
        equipements_data = []

        if commissariat_id and commissariat_id.isdigit():
            # print(f"Commissariat ID: {commissariat_id}")
            equipments = Equipment.objects.filter(commissariat_id=commissariat_id)

        elif etat_civil_id and etat_civil_id.isdigit():
            # print(f"Etat Civil ID: {etat_civil_id}")
            equipments = Equipment.objects.filter(etat_civil_id=etat_civil_id)

        equipements_data = [
            {
                "id": equipment.id,
                "serial_number": equipment.serial_number,
                "type_eq": equipment.type_eq.nom_equipement,
                "brand": equipment.brand,
                "status": equipment.status,
                "modele_eq": equipment.modele_eq,
                "purchase_date": equipment.purchase_date,
                "warranty_expire": equipment.warranty_expire,
            }
            for equipment in equipments
        ]

        # Renvoie une réponse JSON
        return JsonResponse({'equipements_data': equipements_data})
    

class StatisticsView(LoginRequiredMixin, View):

    template_name = 'park/statistics.html'

    def get(self, request, *args, **kwargs):

        # Example data collection
        total_equipments = Equipment.objects.count()
        total_maintenance = Maintenance.objects.count()

        equipments_by_month = (
            Equipment.objects
            .annotate(month=TruncMonth('purchase_date'))  # Regrouper par mois d'achat
            .values('month')
            .annotate(total=Count('id'))  # Compter le nombre d'équipements par mois
            .order_by('month')  # Trier par mois
        )

        # Transformer les données en format JSON pour les utiliser dans le front-end
        
        totals_by_month = [entry['total'] for entry in equipments_by_month]

        # Get equipment by status
        status_counts = Equipment.objects.values('status').annotate(count=models.Count('status'))
        
        status_labels = [entry['status'] for entry in status_counts]  # Statuts : ['en_reparation', 'hors_service', etc.]
        status_values = [entry['count'] for entry in status_counts] 

        total_count = sum(entry['count'] for entry in status_counts)
        status_percentages = [
        {
            'status': entry['status'],
            'percentage': round((entry['count'] / total_count) * 100, 2) if total_count > 0 else 0
        }
        for entry in status_counts
]

        # print(f'label:{status_labels}')
        # print(f'value:{status_values}')
        
        
        # Get counts for each specific status
        en_service_count = Equipment.objects.filter(status='travail').count()
        en_reparation_count = Equipment.objects.filter(status='en_reparation').count()
        en_panne_count = Equipment.objects.filter(status='panne').count()
        hors_service_count = Equipment.objects.filter(status='hors_service').count()

        # Equipment movement data
        movements = EquipmentMovement.objects.count()

        context = {
            'total_equipments': total_equipments,
            'total_maintenance': total_maintenance,
            'status_counts': list(status_counts),  # All status counts
            'movements': movements,
            'en_service_count': en_service_count,  # Total equipment in service
            'en_reparation_count': en_reparation_count,  # Total equipment in repair
            'en_panne_count': en_panne_count,  # Total equipment in panne
            'hors_service_count': hors_service_count,  # Total equipment hors service
            'equipment_monthly_data':totals_by_month,
            'status_labels':status_labels,
            'status_values':status_values,
            'status_percentages': status_percentages,

        }

        return render(request, self.template_name, context)
