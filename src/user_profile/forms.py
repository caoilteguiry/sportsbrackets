from django import forms
from django.contrib.auth.models import User
from models import UserProfile
from django.utils.translation import ugettext as _

MINIMUM_PASSWORD_LENGTH = 6

class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(label="First Name")
    last_name =  forms.CharField(label="Last Name")
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=MINIMUM_PASSWORD_LENGTH, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=MINIMUM_PASSWORD_LENGTH, label="Verify Password")
    
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError(_("A user with this username already exists."))
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError(_("A user with this email address already exists."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields don't match."))
        return password2
    

class MyProfileForm(forms.ModelForm):
    share_predictions = forms.BooleanField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user')