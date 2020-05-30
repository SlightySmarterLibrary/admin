from django.shortcuts import render
from django.conf import settings
from djwarrant.utils import get_cognito


# call dynamo from here
def storeinfo(request):
    store_id = request.user.email

    return render(request, 'warrant/storeinfo.html', {'store_id': store_id})

