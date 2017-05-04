# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import datetime

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
        "date": "December 27th, 2017",
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


# Sends the Tasks in sorted format to calendar.htmls
def calendar(request):
    task_one = {
        "id": 1,
        "user": "Ishaan",
        "name": "Do the laundry",
        "date": "12/25/2017",
        "deadline": "5:30"
    }
    task_two = {
        "id": 2,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "12/25/2017",
        "deadline": "4:30"
    }
    task_three = {
        "id": 3,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "12/27/2017",
        "deadline": "4:30"
    }
    task_four = {
        "id": 4,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "2/25/2017",
        "deadline": "4:30"
    }
    task_five = {
        "id": 5,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "2/25/2017",
        "deadline": "4:30"
    }
    task_six = {
        "id": 6,
        "user": "Ishaan",
        "name": "Assignment 7",
        "date": "1/25/2017",
        "deadline": "4:30"
    }
    task1 = [task_one, task_two,task_three,task_four,task_five, task_six]
    task1 = sort_date(task1)
    task1 = sort_time(task1)
    task_dict = {}
    for t in task1:
        month = getMonth(t["date"].split("/")[0])
        if month in task_dict:
            task_dict[month].append(t)
        else:
            task_dict[month] = []
            task_dict[month].append(t)
    print "Reached Here"
    return render(request, 'calendar.html',context={"task_dict": task_dict},status=200)
# Sort according to Data
def sort_date(list_task):
    for index in range(1, len(list_task)):

        currentvalue = list_task[index]
        position = index

        while position > 0 and int(list_task[position - 1]["date"].split("/")[0]) > int(
                currentvalue["date"].split("/")[0]):
            list_task[position] = list_task[position - 1]
            position = position - 1

            list_task[position] = currentvalue
    return list_task
#Sort according to Time After sorting according to time
def sort_time(list_task):
    for position in range(1, len(list_task)):
        currentvalue = list_task[position]

        if ((int(list_task[position - 1]["date"].split("/")[0]) == int(currentvalue["date"].split("/")[0])) and (
            int(list_task[position - 1]["date"].split("/")[1]) == int(currentvalue["date"].split("/")[1]))):
            if int(list_task[position - 1]["deadline"].split(":")[0]) > int(currentvalue["deadline"].split(":")[0]):
                temp = list_task[position]
                list_task[position] = list_task[position - 1]
                list_task[position - 1] = temp
            elif (int(list_task[position - 1]["deadline"].split(":")[0]) == int(currentvalue["deadline"].split(":")[0])):
                if (int(list_task[position - 1]["deadline"].split(":")[1]) > int(
                        currentvalue["deadline"].split(":")[1])):
                    temp = list_task[position]
                    list_task[position] = list_task[position - 1]
                    list_task[position - 1] = temp

    return list_task
#Convert Numbers to month format
def getMonth(month):
    return datetime.date(1900, int(month), 1).strftime('%B')



