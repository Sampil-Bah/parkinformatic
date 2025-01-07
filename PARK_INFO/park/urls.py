from django.urls import path 

from . import views

app_name = "park"

urlpatterns = [

    path('', views.StatisticsView.as_view(), name='home'),
    path('equipement/', views.EquipementView.as_view(), name='equipement'),
    path('maintenance/', views.MaintenanceView.as_view(), name='maintenance'),
    path('detail/', views.get_detail_modal, name='detail'),
    # path('update/', views.UpdateStatusView.as_view(), name='update'),
    path('search/', views.EquipmentAjaxSearchView.as_view(), name='equipment-ajax-search'),
    path('audit_search/', views.EquipmentMaintenanceSearchView.as_view(), name='audit-ajax-search'),
    path('recherche/', views.HomeView.as_view(), name='recherche'),
    path('location/', views.LocationsView.as_view(), name='location'),
    path('audit/', views.AuditView.as_view(), name='audit'),
]