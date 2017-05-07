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
    username = request.session['username']
    tasks = dynamo.tasks_list(username)
    for task in tasks:
        task['readable_deadline'] = _iso_datetime_to_human_readable(task['deadline'])
    return render(request, 'edit.html', context={
        "tasks": tasks
    }, status=200)



@csrf_exempt
def reprioritize(request):
    username = request.session['username']
    ids = json.loads(request.POST['task_ids'])
    print ids
    for i in range(len(ids)):
        ids[i] = int(ids[i])
    dynamo.task_update_all_priority(username, ids, all_tasks = False)
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

@csrf_exempt
def blowup_save(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    username = request.session['username']
    task = json.loads(request.POST['task'])
    print task
    task_id = task["task_id"]
    print task
    dynamo.task_update(username, task_id, task)
    return HttpResponse(status=200)


def save(request, task_id):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    print task_id
    print request.POST

    username = request.session['username']
    
    #TODO Fix modal to delete this fix.
    if 'ud_priority' in request.POST:
        priority = request.POST['ud_priority']
    else:
        priority = 2
        
    time = request.POST['ud_time']
    deadline = request.POST['deadline']
    item = request.POST['item']
    description = request.POST['description']
    task = {
       'ud_priority': priority,
       'ud_time': time,
       'deadline': deadline,
       'item': item,
       'description': description,
    }

    dynamo.task_update(username, task_id, task)
    return HttpResponseRedirect(reverse('taskpop:edit'))


def blowup(request, task_id):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    username = request.session['username']
    tasks = dynamo.task_blowup(username, task_id)
    return render(request, 'blowup.html', context={
        "tasks": tasks
    })


@csrf_exempt
def delete(request, task_id):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    username = request.session['username']
    dynamo.task_remove(username, int(task_id))
    return HttpResponseRedirect(reverse('taskpop:edit'))


def calendar(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse('taskpop:login'))
    username = request.session['username']
    user = dynamo.tasks_get(username)
    multiplier = user['multiplier']

    tasks = dynamo.tasks_list(username)
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
    return render(request, 'calendar.html',context={
        "task_dict": task_dict,
        "multiplier": multiplier}, status=200)


def get_month(month):
    return datetime.date(1900, int(month), 1).strftime('%B')


def settings(request):
    return render(request,'settings.html')
