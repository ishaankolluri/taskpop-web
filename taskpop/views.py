# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect, reverse


# Create your views here.


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def edit(request):
    print request.GET
    # TODO: Request tasks associated with the user key(requests) from Dynamo.
    # TODO: Build the task list and pass it to edit.html.
    # TODO: Investigate the format of the task returned to Django from AWS.
    # Below is a sample task list. NOTE: This could be incorrect JSON.
    task_one = {
        "user": "Ishaan",
        "task_name": "Do the laundry",
        "due_date": "December 25th, 2017",
        "deadline": "5:30pm"
    }
    task_two = {
        "user": "Ishaan",
        "task_name": "Assignment 7",
        "due_date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    task_three = {
        "user": "Ishaan",
        "task_name": "Assignment 7",
        "due_date": "December 25th, 2017",
        "deadline": "4:30pm"
    }
    tasks = [task_one, task_two, task_three]

    return render(request, 'edit.html', context={
            "user": task_one["user"],
            "tasks": tasks
    })


def logout(request):
    # The OAuth should already have handled this.
    return HttpResponseRedirect(reverse('taskpop:login'))
