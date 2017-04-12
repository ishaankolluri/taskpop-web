# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect, reverse


# Create your views here.


def login(request):
    return render(request, 'login.html')


def home(request):
    print "Reached the home request"
    print request.__dict__
    # This is only if the user has been unauthenticated.
    return HttpResponseRedirect(reverse('taskpop:login'))

    # return HttpResponseRedirect(reverse('taskpop:')


def logout(request):
    # The OAuth should already have handled this.
    return HttpResponseRedirect(reverse('taskpop:login'))
