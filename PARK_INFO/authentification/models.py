from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password, **kwargs):
        if not email:
            raise ValueError("Email must be set")
        if not first_name:
            raise ValueError("First name must be set")
        if not last_name:
            raise ValueError("Last name must be set")
        
        username = (first_name + last_name).lower()

        user = self.model(
            email=self.normalize_email(email), 
            first_name=first_name,
            last_name=last_name,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, first_name, last_name, password, **kwargs)

class User(AbstractUser):  

    """ 
        Name: User Model (Technicians or Admins)
        Description: Stores information about users responsible for managing or maintaining equipment.
        Author: sampilbah@gmail.com
    """

    ROLE_CHOICES = [
        ('Technicien', 'Technicien'),
        ('Manager', 'Manager'),
    ]

    role                = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="User Role")
    email               = models.EmailField(unique=True, verbose_name="Email Address")
    is_approved         = models.BooleanField(default=False, verbose_name="Approved by Admin")

    REQUIRED_FIELDS = ["last_name", "first_name", "username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['first_name']
