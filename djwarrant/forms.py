from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=30, required=False)
    gender = forms.ChoiceField(
        choices=(('female', 'Female'), ('male', 'Male')), required=False)
    address = forms.CharField(max_length=200, required=False)
    preferred_username = forms.CharField(max_length=200, required=False)
    api_key = forms.CharField(max_length=200, required=False)
    api_key_id = forms.CharField(max_length=200, required=False)


class APIKeySubscriptionForm(forms.Form):
    plan = forms.ChoiceField(required=True)

    def __init__(self, plans=[], users_plans=[], *args, **kwargs):
        self.base_fields['plan'].choices = [
            (p.get('id'), p.get('name')) for p in plans if not p.get('id') in users_plans]
        super(APIKeySubscriptionForm, self).__init__(*args, **kwargs)


class AccountVerificationForm(forms.Form):
    """Verifies a user to create their account"""
    username = forms.CharField()
    confirmation_code = forms.CharField(
        required=True, max_length=6, label="Verification Code")

    def clean(self):
        user = super(AccountVerificationForm, self).clean()
        self.user = user

        return user


class SignUpForm(forms.Form):
    """Specifies required information for user sign up"""
    username = forms.CharField(max_length=100, required=True)
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    verify_password = forms.CharField(
        widget=forms.PasswordInput(), required=True)

    def clean(self):
        user = super(SignUpForm, self).clean()
        self.user = user

        if user.get('password') != user.get('verify_password'):
            self.errors['verify_password'] = \
                self.error_class(['Passwords do not match'])
            del self.user['password']

        del self.user['verify_password']

        return user
