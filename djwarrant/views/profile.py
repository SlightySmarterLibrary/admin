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

    def create_store(store_id, name, address, adults, children):
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        sns = boto3.client('sns')
    
        topicname = store_id + name
        topicname = ''.join(e for e in topicname if e.isalnum())
        topicname = topicname.replace(" ", "")


        # create arn
        topic = sns.create_topic(Name=topicname)
        arn = topic['TopicArn']

        # create table
        try:
            dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S',
                    },
                ],
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH',
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                },
                TableName='stores',
            )
            dynamodb.get_waiter('table_exists').wait(TableName='HW2')
        except dynamodb.exceptions.ResourceInUseException:
            pass
        except Exception as e:
            print("Error creating table.")
            print(e)

        # add store
        dynamodb.put_item(
                TableName='stores',
                Item= {
                    "id": {"S": f"{store_id}"}, 
                    "name":{"S": f"{name}"},
                    "adult": {"N": f"{adults}"},
                    "children":{"N": f"{children}"},
                    "address":{"S": f"{address}"},
                    "sns_arn":{"S": f"{arn}"}
                }
            )



    def form_valid(self, form):
        cognito = CognitoBackend()
        

        try:
            resp = cognito.register(name=form.user['name'], password=form.user['password'],
                                    email=form.user['email'], username=form.user['username'])
            # create store
            # store_id = str(uuid.uuid4()) #Unique identifier for store
            SignUpView.create_store(form.user['email'], form.user['name'], form.user['address'], form.user['adult_masks'], form.user['children_masks'])

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
            print(resp)
        except Exception as e:
            print(e)
            pass

        return super().form_valid(form)
