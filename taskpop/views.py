# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect, reverse


# Create your views here.


def login(request):
    return render(request, 'login.html')


def home(request):
    print request
    return render(request, 'home.html')


    # return HttpResponseRedirect(reverse('taskpop:')

def logout(request):
    # The OAuth should already have handled this.
    return HttpResponseRedirect(reverse('taskpop:login'))
