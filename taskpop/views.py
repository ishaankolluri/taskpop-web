# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt

from . import dynamo


def process_datetime(datetime_local_html):
    # TODO: This function.
    print datetime_local_html
    # Input: MM/DD/YYYY, XX:YY MM
    # Output: ISO 8601 Format for JSON
    return datetime_local_html


def datetime_to_html(json_datetime):
    # TODO: This function. Must output to HTML form correctly.
    print json_datetime
    # Input: ISO 8601 Format for JSON
    # Output: MM/DD/YYYY, XX:YY MM
    return json_datetime


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
    dynamo.tasks_create(username)
    return HttpResponse(status=200)


def login(request):
    return render(request, 'login.html')


def home(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    username = request.session['username']
    # tasks = dynamo.tasks_list(username, 3)
    # TODO: Note they come with more features, but we only use the following.
    task_one = {
        "task_id": 1,
        "item": "Do the laundry",
        "date": "December 25th, 2017",
        "deadline": "5:30pm"
    }
    task_two = {
        "task_id": 2,
        "item": "Assignment 7",
        "date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    task_three = {
        "task_id": 3,
        "item": "Assignment 7",
        "date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    tasks = [task_one, task_two, task_three]

    return render(request, 'home.html', context={
        "username": username,
        "tasks": tasks,
    })


def edit(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    # tasks = dynamo.tasks_list(username)
    
    task_one = {
        "task_id": 1,
        "item": "Do the laundry",
        "deadline": "1994-12-30",  # TODO: This needs to be decoded.
        "time": "5:30pm",
        "description": "Sample Description 1",
        "ud_priority": 4,
        "ud_time": 7,
    }
    task_two = {
        "task_id": 2,
        "item": "Assignment 7",
        "deadline": "December 25th, 2017",
        "time": "4:30pm",
        "description": "Sample Description 2",
        "ud_priority": 3,
        "ud_time": 5,
    }
    task_three = {
        "task_id": 3,
        "item": "Assignment 7",
        "deadline": "December 25th, 2017",
        "time": "4:30pm",
        "description": "Sample Description 3",
        "ud_priority": 1,
        "ud_time": 2,
    }
    tasks = [task_one, task_two, task_three]
    return render(request, 'edit.html', context={
        "tasks": tasks
    }, status=200)


def logout(request):
    # The OAuth should already have handled this.
    return HttpResponseRedirect(reverse('taskpop:login'))


def create(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    print request.POST
    username = request.session['username']
    priority = request.POST['priority']
    time = request.POST['time']
    deadline = request.POST['deadline']
    deadline = process_datetime(deadline)
    item = request.POST['name']
    description = request.POST['description']
    task = {
       'ud_priority': priority,
       'ud_time': time,
       'deadline': deadline,
       'item': item,
       'description': description,
    }
    # dynamo.task_new(username, task)
    return HttpResponseRedirect(reverse('taskpop:home'))


def complete(request, task_id):
    username = request.session['username']
    completed_time = int(request.POST['task_duration'])
    # dynamo.task_archive(username, task_id, completed_time):
    return HttpResponseRedirect(reverse('taskpop:home'))


def save(request, task_id):
    print task_id
    print request.POST
    # TODO: update the task at task_id with the contents of request.POST


    username = request.session['username']
    #task = {
    #    'ud_priority': # int 0-4,
    #    'ud_time': # int in hours,
    #    'deadline': # date time in ISO FORMAT,
    #    'item': String,
    #    'description': String
    #}     
    # dynamo.task_update(username, task_id, task)
    
    
    return HttpResponseRedirect(reverse('taskpop:edit'))


def blowup(request, task_id):
    # TODO: new page for blowup.
    print task_id
    
    username = request.POST['username']
    #dynamo.task_blowup(username, task_id)
    
    
    return HttpResponseRedirect(reverse('taskpop:edit'))


@csrf_exempt
def delete(request, task_id):
    print task_id
    # print json.loads(request.POST['json_data'])['tasks']
    # NOTE: This might not redirect because it calls back to the AJAX in JS.
    
    #dynamo.task_remove(username, task_id)
    
    return HttpResponseRedirect(reverse('taskpop:edit'))
