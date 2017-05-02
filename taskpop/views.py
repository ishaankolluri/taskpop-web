# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def edit(request):
    print "hit edit"
    # TODO: Request tasks associated with the user key(requests) from Dynamo.
    # TODO: Build the task list and pass it to edit.html.
    # TODO: Investigate the format of the task returned to Django from AWS.
    # Below is a sample task list. NOTE: This could be incorrect JSON.
    task_one = {
        "id": 1,
        "user": "Ishaan",
        "name": "Do the laundry",
        "date": "December 25th, 2017",
        "deadline": "5:30pm"
    }
    task_two = {
        "id": 2,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    task_three = {
        "id": 3,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    tasks = [task_one, task_two, task_three]
    print "rendering"
    return render(request, 'edit.html', context={
        "user": task_one["user"],
        "tasks": tasks
    }, status=200)


def logout(request):
    # The OAuth should already have handled this.
    return HttpResponseRedirect(reverse('taskpop:login'))


def create(request):
    print request.POST
    # TODO: Unpack the contents of the POST request
    # select what we need and pack into JSON
    # send JSON to dynamo /create_task/ endpoint
    # upon successful POST, redirect to home.

    return HttpResponseRedirect(reverse('taskpop:home'))


def complete(request, task_id):
    print "Checking success"
    print task_id
    # TODO: Send a 'complete_task' request to Dynamo for this task_id
    # TODO: Lambda will do any other calculations.

    return HttpResponseRedirect(reverse('taskpop:home'))


def save(request, task_id):
    print task_id
    print request.POST
    # TODO: update the task at task_id with the contents of request.POST
    return HttpResponseRedirect(reverse('taskpop:edit'))


def blowup(request, task_id):
    # TODO: new page for blowup.
    print task_id
    return HttpResponseRedirect(reverse('taskpop:edit'))


@csrf_exempt
def delete(request):
    print "Hit delete"
    print json.loads(request.POST['json_data'])['tasks']
    # NOTE: This might not redirect because it calls back to the AJAX in JS.
    return HttpResponseRedirect(reverse('taskpop:edit'))


def calendar(request):
    print "Reached Here"
    return render(request, 'calendar.html')
