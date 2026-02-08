from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.Form):
    username = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control',
                                                                        'placeholder':'Username'}))
    email = forms.EmailField(label= '', widget=forms.TextInput(attrs={'class':'form-control',
                                                                      'placeholder':'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'placeholder':'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'placeholder':'Confirm Password'}))
      
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("this email already exists")
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("this username already exists")
        return username
        
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords must match.')
        return 
    

class UserLoginForm(forms.Form):
     username = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control',
                                                                        'placeholder':'Username'}))
     password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'placeholder':'Password'}))
     

class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label= '', widget=forms.TextInput(attrs={'class':'form-control',
                                                                        'placeholder':'Email'}))

    class Meta:
        model = Profile
        fields = ('age', 'bio', 'pict')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''
        
        self.fields['age'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Age'})
        self.fields['bio'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Bio'})
        self.fields['pict'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Profile picture'})