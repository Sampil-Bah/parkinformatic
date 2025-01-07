from django.db import models
from django.utils import timezone

from authentification.models import *


class Direction(models.Model):
    name = models.CharField(max_length=50)


class Region(models.Model):

    region          = models.CharField(max_length=100)

    def __str__(self):
        return self.region


class Prefecture(models.Model):
   
    region                           = models.ForeignKey(Region, on_delete=models.CASCADE)
    prefecture                       = models.CharField(max_length=100)
    
    def __str__(self):
        return self.prefecture
    

class EtatCivil(models.Model):
    
    """
        Name:
        Description: ce model decrits les etats civils dans les quels sont confectionnés les extraits biometriques
        Author: sampilbah@gmail.com
    """

    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    etat_civil = models.CharField(max_length=150)

    def __str__(self):
        return self.etat_civil
    

class Commissariat(models.Model):
    
    """
        Name: Commissariat  
        Description: ce model decrit les commissariats centraux dans les quels on fait l'enrollemnt pour la carte biometrique
        Author: sampilbah@gmail.com
    """
    prefecture              = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    commissariat            = models.CharField(max_length=150)

    def __str__(self):
        return self.commissariat


class Location(models.Model):

    """ 
        Name: Location Model 
        Description: stores where the materials are located
        Author: sampilbah@gmail.com
    """
    name                       = models.CharField(max_length=100)
    address                    = models.CharField(max_length=255)

    class Meta:
        verbose_name        = 'Location'
        verbose_name_plural = 'Locations'    

    def __str__(self):
        return self.name
    
class TypeEquipement(models.Model):

    nom_equipement          = models.CharField(max_length=150)

    def __str__(self):
        return self.nom_equipement


class Equipment(models.Model):

    """ 
        Name: Equipment Model
        Description: Stores details of each equipment and its current status.
        Author: sampilbah@gmail.com
    """

    # Define status choices
    STATUS_CHOICES = [
        ('travail', 'Travail'),
        ('en_reparation', 'En reparation'),
        ('hors_service', 'Hors Service'),
        ('panne', 'En panne'),
    ]

    serial_number                       = models.CharField(max_length=50, unique=True, verbose_name="Serial Number")
    type_eq                             = models.ForeignKey(TypeEquipement, on_delete=models.CASCADE)
    brand                               = models.CharField(max_length=50, verbose_name="Brand")
    modele_eq                           = models.CharField(max_length=50, verbose_name="Model")
    purchase_date                       = models.DateField(verbose_name="Purchase Date")
    warranty_expire                     = models.DateField(verbose_name="Warranty Expiry Date")
    status                              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='working', verbose_name="Status")
    commissariat                        = models.ForeignKey(Commissariat, on_delete=models.SET_NULL, null=True, blank=True)
    etat_civil                          = models.ForeignKey(EtatCivil, on_delete=models.SET_NULL, null=True, blank=True)
    direction                           = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.type} ({self.serial_number}) - {self.get_status_display()}"


    class Meta:
        verbose_name        = 'Equipment'
        verbose_name_plural ='Equipments'

    def __str__(self):
        return f"{self.brand} {self.modele_eq} ({self.serial_number})"


class Maintenance(models.Model):

    """ 
        Name: Maintenance Model 
        Description: 
        Author: sampilbah@gmail.com    
    """

    equipment                       = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    technician                      = models.ForeignKey(User, on_delete=models.CASCADE)
    maintenance_date                = models.DateField(default=timezone.now)
    issue_description               = models.TextField()
    action_taken                    = models.TextField()

    class Meta:
        verbose_name                = 'Maintenance'
        verbose_name_plural         = 'Maintenances'

    def __str__(self):
        return f"Maintenance for {self.equipment.serial_number} on {self.maintenance_date}"


class EquipmentMovement(models.Model):

    """ 
        Name: Equipment Movement Model 
        Description:
        Author: sampilbah@gmail.com    
    """

    equipment                           = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    from_location                       = models.ForeignKey(Location, related_name='from_location', on_delete=models.CASCADE)
    to_location                         = models.ForeignKey(Location, related_name='to_location', on_delete=models.CASCADE)
    movement_date                       = models.DateField(default=timezone.now)

    class Meta:
        verbose_name                    = 'EquipmentMovement'
        verbose_name_plural             = 'EquipmentMovements'

    def __str__(self):
        return f"Moved {self.equipment.serial_number} from {self.from_location} to {self.to_location}"


class AuditLog(models.Model):

    """ 
        Name: AuditLog Model 
        Description:
        Author: sampilbah@gmail.com    
    """

    action                              = models.CharField(max_length=255)
    equipment                           = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    performed_by                        = models.ForeignKey(User, on_delete=models.CASCADE)
    date_performed                      = models.DateField(default=timezone.now)

    class Meta:
        verbose_name        = 'AuditLog'
        verbose_name_plural = 'AuditLogs'

    def __str__(self):
        return f"{self.action} on {self.equipment.serial_number}"
