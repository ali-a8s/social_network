from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;'}))


    def clean_email(self): 
        email = self.cleaned_data['email']
        user = User.objects.filter(email= email)

        if user.exists():
            raise ValidationError('this email already exists')
        return email

    def clean_username(self): 
        username = self.cleaned_data['username']
        user = User.objects.filter(username= username)

        if user.exists():
            raise ValidationError('this username already exists')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd['password1']
        p2 = cd['password2']

        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords must match')



class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;'}))



class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['age', 'bio']