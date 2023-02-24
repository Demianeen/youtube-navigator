from django import forms
from .models import MyUser

class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control',
                                                             'style':'width: 300px; margin: auto;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                             'style':'width: 300px; margin: auto;'}))
    class Meta():
        model = MyUser
        fields = ('email','password')

