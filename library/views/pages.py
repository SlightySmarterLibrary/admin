from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('book_index'))

    return render(request, 'index.html')
