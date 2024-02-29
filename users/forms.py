from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from .models import User


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        label='Email Address',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False

        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary btn-md px-4 mt-3'))



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, label='Username', max_length=100, help_text='')
    email = forms.EmailField(required=True, label='Email Address', max_length=100, help_text='')
    first_name = forms.CharField(required=True, label='First Name', max_length=100, help_text='')
    last_name = forms.CharField(required=True, label='Last Name', max_length=100, help_text='')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        #self.fields['username'].help_text = 'Required. 150 characters or fewer.'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            print('saved!')
            user.save()
        else:
            print('not saved!')
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }