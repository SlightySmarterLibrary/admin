from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
try:
    from django.urls import reverse_lazy, reverse
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.contrib.auth.views import LogoutView as DJLogoutView
from django.conf import settings
from django.shortcuts import render
from djwarrant.utils import get_cognito
from djwarrant.forms import ProfileForm
from ..forms import SignUpForm, AccountVerificationForm
from warrant import Cognito
from djwarrant.backend import CognitoBackend
import boto3
import uuid
import json
from library.utils.dynamo_helpers import create_user


class TokenMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('REFRESH_TOKEN'):
            return self.handle_no_permission()
        return super(TokenMixin, self).dispatch(
            request, *args, **kwargs)


class GetUserMixin(object):

    def get_user(self):
        c = get_cognito(self.request)
        return c.get_user(attr_map=settings.COGNITO_ATTR_MAPPING)


class ProfileView(LoginRequiredMixin, TokenMixin, GetUserMixin, TemplateView):
    template_name = 'warrant/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context


class UpdateProfileView(LoginRequiredMixin, TokenMixin, GetUserMixin, FormView):
    template_name = 'warrant/update-profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('dw:profile')

    def get_initial(self):
        u = self.get_user()
        return u.__dict__.get('_data')

    def form_valid(self, form):
        c = get_cognito(self.request)
        c.update_profile(form.cleaned_data, settings.COGNITO_ATTR_MAPPING)
        messages.success(
            self.request, 'You have successfully updated your profile.')
        return super(UpdateProfileView, self).form_valid(form)


class LogoutView(DJLogoutView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.delete()
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


class SignUpView(FormView):
    template_name = 'warrant/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        cognito = CognitoBackend()

        try:
            # Register user to cognito
            resp = cognito.register(name=form.user['name'], password=form.user['password'],
                                    email=form.user['email'], username=form.user['username'])
            # Create user in DynamoDB
            create_user(id=resp['UserSub'], username=form.user['username'], name=form.user['name'],
                        email=form.user['email'], role="admin", library=form.user['library_name'])
        except Exception as e:
            if "User already exists" in str(e):
                form.errors['username'] = form.error_class(
                    ['The provided username is already in use'])
                return self.form_invalid(form)

            elif "Password did not conform with the policy" in str(e):
                forms.errors['username'] = form.error_class(
                    ['The password provided is invalid'])
                return self.form_invalid(form)

            else:
                raise(e)

        return HttpResponseRedirect(reverse('dw:account_verification',
                                            kwargs={'username': form.user['username']}))


class AccountVerificationView(FormView):
    template_name = 'warrant/account_verification.html'
    form_class = AccountVerificationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.kwargs.get('username', '')

        return initial

    def get_success_url(self):
        return resolve_url('/')

    def form_valid(self, form):
        cognito = CognitoBackend()

        try:
            resp = cognito.validate_user(**form.user)
        except Exception as e:
            pass

        return super().form_valid(form)
