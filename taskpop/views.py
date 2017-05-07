# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt

from . import dynamo


def _iso_datetime_to_human_readable(datetime_str):
    datetime_str = datetime_str.split('T')
    date = datetime_str[0].split('-')
    time = datetime_str[1].split(':')

    year = date[0]
    month = date[1]
    day = date[2]

    hour = time[0]
    minute = time[1]
    am_pm = 'AM'

    if int(hour) > 12:
        hour = str(int(hour) -12)
        am_pm = 'PM'

    return '%s/%s/%s %s:%s %s' % (month, day, year, hour, minute, am_pm)


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


@csrf_exempt
def firsttimeuser(request):
    print "Adding a first time user..."
    username = request.POST['username']
    dynamo.tasks_create(username)
    return HttpResponse(status=200)


def login(request):
    return render(request, 'login.html')


def home(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    username = request.session['username']
    
    tasks = dynamo.tasks_list(username, 3)
        
    for task in tasks:
        task['readable_deadline'] = _iso_datetime_to_human_readable(task['deadline'])

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
        "deadline": "1994-12-30T05:30",  # TODO: This needs to be decoded.
        "description": "Urgent. Dry Wash the Jacket",
        "ud_priority": 4,
        "ud_time": 7,
    }
    task_two = {
        "task_id": 2,
        "item": "Assignment 7",
        "deadline": "2017-12-25T04:30",
        "description": "Write the documentation of the code",
        "ud_priority": 3,
        "ud_time": 5,
    }
    task_three = {
        "task_id": 3,
        "item": "ML",
        "deadline": "2017-12-25T04:30",
        "description": "Work on SVMs",
        "ud_priority": 1,
        "ud_time": 2,
    }
    tasks = [task_one, task_two, task_three]
    for task in tasks:
        task['readable_deadline'] = _iso_datetime_to_human_readable(task['deadline'])
    return render(request, 'edit.html', context={
        "tasks": tasks
    }, status=200)



@csrf_exempt
def reprioritize(request):
    username = request.session['username']
    ids = json.loads(request.POST['task_ids'])
    for i in range(len(ids)):
        ids[i] = int(ids[i])

    # dynamo.task_update_priority(username, ids)
    # TODO(keir): this would be the new function signature.
    return HttpResponse(status=200)


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
    item = request.POST['name']
    description = request.POST['description']
    task = {
       'ud_priority': priority,
       'ud_time': time,
       'deadline': deadline,
       'item': item,
       'description': description,
    }
    dynamo.task_new(username, task)
    return HttpResponseRedirect(reverse('taskpop:home'))


def complete(request, task_id):
    username = request.session['username']
    completed_time = int(request.POST['task_duration'])
    dynamo.task_archive(username, task_id, completed_time)
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
    
    username = request.session['username']
    #dynamo.task_blowup(username, task_id)
    
    
    return HttpResponseRedirect(reverse('taskpop:edit'))


@csrf_exempt
def delete(request, task_id):
    print task_id
    # print json.loads(request.POST['json_data'])['tasks']
    # NOTE: This might not redirect because it calls back to the AJAX in JS.
    
    #dynamo.task_remove(username, task_id)
    
    return HttpResponseRedirect(reverse('taskpop:edit'))


# Sends the Tasks in sorted format to calendar.html
def calendar(request):
    task_one = {
        "task_id": 1,
        "item": "Do the laundry",
        "deadline": "2017-12-30T04:30",  # TODO: This needs to be decoded.
        "description": "Urgent. Dry Wash the Jacket ",
        "ud_priority": 4,
        "ud_time": 7,
    }

    task_two = {
        "task_id": 1,
        "item": "ML HW",
        "deadline": "2017-12-30T03:30",  # TODO: This needs to be decoded.
        "description": "Redo the SVM Algorithm",
        "ud_priority": 4,
        "ud_time": 7,
    }
    task_three = {
        "task_id": 1,
        "item": "Algo Course",
        "deadline": "2017-11-30T03:00",  # TODO: This needs to be decoded.
        "description": "  Algorithm chapter 5",
        "ud_priority": 4,
        "ud_time": 7,
    }
    task_four = {
        "task_id": 1,
        "item": "Do the laundry",
        "deadline": "2017-12-28T04:30",  # TODO: This needs to be decoded.
        "description": "Sample Description 1",
        "ud_priority": 4,
        "ud_time": 7,
    }
    task_five = {
        "task_id": 1,
        "item": "Do the laundry",
        "deadline": "2017-11-30T17:30",  # TODO: This needs to be decoded.
        "description": "Sample Description 1",
        "ud_priority": 4,
        "ud_time": 7,
    }
    task_six = {
        "task_id": 1,
        "item": "Finish of the book",
        "deadline": "2017-01-15T20:00",  # TODO: This needs to be decoded.
        "description": "Work on the text",
        "ud_priority": 4,
        "ud_time": 7,
    }

    tasks = [task_one, task_two,task_three,task_four,task_five, task_six]
    tasks = sorted(tasks, key=lambda k: k['deadline'])
    task_dict = {}
    for task in tasks:
        month = get_month(task["deadline"].split("-")[1])
        task['readable_deadline'] = _iso_datetime_to_human_readable(task['deadline'])
        if month in task_dict:
            task_dict[month].append(task)
        else:
            task_dict[month] = []
            task_dict[month].append(task)
    return render(request, 'calendar.html',context={"task_dict": task_dict},status=200)


def get_month(month):
    return datetime.date(1900, int(month), 1).strftime('%B')


def settings(request):
    return render(request,'settings.html')
