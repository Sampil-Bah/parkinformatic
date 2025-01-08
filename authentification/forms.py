from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Entrer votre email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Entrer votre prenom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Entrer votre nom'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "The two password fields didn’t match.")

        return cleaned_data

    def save(self, commit=True):
        """
        Override the save method to handle password hashing for the User model.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user
