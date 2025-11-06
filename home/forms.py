from django import forms 
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']



class CommenCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 250px;'})
        }



class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 250px;', 'placeholder': 'search in titles and bodies'}))
