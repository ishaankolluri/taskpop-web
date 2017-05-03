# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def deauth(request):
    request.session['username'] = None
    return HttpResponse(status=204)


@csrf_exempt
def session(request):
    print "auth session"
    current_user = request.POST['username']
    if current_user not in request.session:
        request.session['username'] = current_user
    print request.session['username']
    return HttpResponse(status=204)


def firsttimeuser(request):
    username = request.POST['username']
    tasks_create(username)
    return HttpResponse(status=200)


def login(request):
    return render(request, 'login.html')


def home(request):
    # if 'username' not in request.session:
    #     return HttpResponseRedirect(reverse('taskpop:login'))
    # TODO Query top three. Provide as context.
    username = request.session['username']
    return render(request, 'home.html', context={
        "username": username
    })


def edit(request):
    print "hit edit"
    # TODO: Request tasks associated with the user key(requests) from Dynamo.
    # TODO: Build the task list and pass it to edit.html.
    # TODO: Investigate the format of the task returned to Django from AWS.
    # Below is a sample task list. NOTE: This could be incorrect JSON.
    task_one = {
        "task_id": 1,
        "user": "Ishaan",
        "name": "Do the laundry",
        "date": "December 25th, 2017",
        "deadline": "5:30pm"
    }
    task_two = {
        "task_id": 2,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    task_three = {
        "task_id": 3,
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
    print request.session['username']
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
def delete(request, task_id):
    print task_id
    # print json.loads(request.POST['json_data'])['tasks']
    # NOTE: This might not redirect because it calls back to the AJAX in JS.
    return HttpResponseRedirect(reverse('taskpop:edit'))
