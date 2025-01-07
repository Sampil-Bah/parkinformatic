from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views import View

from django.urls import reverse_lazy

from .models import User

from .forms import UserForm
from .models import *

class HomeView(View):
    
    """
        this is the authentication home view where 
        the user get authenticated to access the home page
    """

    template_name = 'authentification/index.html' 

    def get(self,request, *args, **kwargs):

        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, self.template_name, {'error': 'Invalid email or password'})

        # Vérifie si le mot de passe est correct
        if user.check_password(password):
            print('Password is correct')
        else:
            return render(request, self.template_name, {'error': 'Invalid email or password'})

        print(f'user : {user}')
        # Authentifie l'utilisateur
        # user = authenticate(request, username=username, password=password)
        # print(f'Authenticated User: {user}')

        if user is not None:
            login(request, user)
            return redirect('park:home')

        context = {
            'error': 'Invalid username or password'
        }
        return render(request, self.template_name, context)


    

class SigninView(View):

    template_name = 'authentification/signin.html'

    def get(self, request, *args, **kwargs):

        form = UserForm()

        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):

        form = UserForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            confirmed_password = request.POST.get('confirm_password')

            username = (first_name + last_name).lower()

            # Create the user using the custom manager
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                username=username,
            )
            user.is_active = False

            user.save()

            messages.success(request, "Votre compte a été créé avec succès ! En attente d'approbation par l'admin.")
            return redirect('authentification:login')

        else:
            return render(request, self.template_name, context={"form": form})
     
# @require_POST
def logout_view(request):
    logout(request)
    return redirect('authentification:login')
        
    
       
