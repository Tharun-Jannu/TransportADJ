from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from datetime import date
from django.forms.widgets import PasswordInput


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            from .models import Customer

            Customer.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"],
                address=self.cleaned_data["address"],
                date_of_birth=self.cleaned_data["date_of_birth"],
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TelInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=PasswordInput(attrs={"class": "form-control"}))
