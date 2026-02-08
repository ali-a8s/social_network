from django import forms 
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''
        
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Title'})
        self.fields['body'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Content'})


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.fields['body'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Write your comment here...'})


class PostSearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control',
                                                                     'placeholder': 'search in titles and bodies'}))