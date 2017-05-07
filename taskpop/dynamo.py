import boto3
from datetime import datetime
from decimal import *
import json
import random
from operator import attrgetter

# Load all of the tables

with open('dynamodb_keys.json','r') as f:
    dynamodb_keys = json.loads(f.read())

session = boto3.Session(
    aws_access_key_id=dynamodb_keys['aws_access_key_id'],
    aws_secret_access_key=dynamodb_keys['aws_secret_access_key']
)


from boto3.dynamodb.types import DYNAMODB_CONTEXT
# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[Rounded] = 0

dynamodb = session.resource('dynamodb', region_name='us-east-1')

task = dynamodb.Table('task')
tasks = dynamodb.Table('tasks')
tasksarchive = dynamodb.Table('tasksarchive')


def _taskarchive_create(username):
    tasksarchive.put_item(
        Item={
            'username': username,
            'created': datetime.utcnow().isoformat(),
            'tasks': []
        }
    )
    return


def tasks_create(username):
    tasks.put_item(
        Item={
            'username': username,
            'first_name': " ",
            'last_name': " ",
            'created': datetime.utcnow().isoformat(),
            'multiplier': Decimal(1),
            'next_task_num': 1,
            'tasks': list()
        }
    )

    _taskarchive_create(username)

    return


def tasks_get(username):
    response = tasks.get_item(
        Key={
            'username': username,
        }
    )
    if 'Item' in response:
        return response['Item']
    else:    
        tasks_create(username)
        return tasks_get(username)
    

'''
def _tasks_get_next_task_num(username):
    response = tasks.get_item(
        Key={
            'username': username,
        }
    )
    return response['Item']['next_task_num']
'''


def _tasks_update_new_task(username):
    # Returns the task_id that should be added.  Ensures tasks are added sequentially.s
    response = tasks.get_item(
        Key={
            'username': username,
        }
    )
    res = response['Item']
    task_id = res['next_task_num']
    task_list = res['tasks']
    if len(task_list) == 0:
        task_list = [task_id]
    else:
        task_list.append(task_id)

    tasks.update_item(
        Key={
            'username': username,
        },
        UpdateExpression='SET next_task_num = :val1, tasks = :val2',
        ExpressionAttributeValues={
            ':val1': res['next_task_num'] + 1,
            ':val2': task_list
        }
    )
    return task_id


def _tasks_update_remove_task(username, task_id):
    response = tasks.get_item(
        Key={
            'username': username,
        }
    )
    res = response['Item']

    task_list = res['tasks']
    print(task_id)
    task_list.remove(Decimal(task_id))

    tasks.update_item(
        Key={
            'username': username,
        },
        UpdateExpression='SET tasks = :val1',
        ExpressionAttributeValues={
            ':val1': task_list
        }
    )
    return


def _taskarchive_delete(username):
    tasksarchive.delete_item(
        Key={
            'username': username,
        }
    )


def _tasks_delete(username):
    tasks.delete_item(
        Key={
            'username': username,
        }
    )


def user_delete(username):
    # Destroy all tasks everywhere
    pass


def task_new(username, taskarg):
    """
    taskarg = {
        'ud_priority': # int 0-4,
        'ud_time': # int in hours,
        'deadline': # date time in ISO FORMAT,
        'item': String,
        'description': String
    } 

    """
    
    if len(taskarg['description']) == 0:
        taskarg['description'] = 'No description'
    
    task_id = _tasks_update_new_task(username)
    task.put_item(
        Item={
            'username': username,
            'task_id': task_id,
            'created': datetime.utcnow().isoformat(),
            'modified': datetime.utcnow().isoformat(),
            'finished': datetime.utcnow().isoformat(),
            'comp_time': Decimal(1.1),
            'adj_priority': Decimal(taskarg['ud_priority']),
            'ud_priority': taskarg['ud_priority'],
            'ud_time': Decimal(taskarg['ud_time']),
            'deadline': taskarg['deadline'],
            'item': taskarg['item'],
            'description': taskarg['description']
        }
    )
    return task_id


def task_get(username, task_id):
    response = task.get_item(
        Key={
            'username': username,
            'task_id': task_id
        }
    )
    if 'Item' not in response:
        return {}
    return response['Item']


def task_update(username, task_id, taskarg):
    # Just overwrite the values.  Have Django get into a form then push the whole things back in.
    task_id = int(task_id)
    response = task.get_item(
        Key={
            'username': username,
            'task_id': task_id
        }
    )
    res = response['Item']

    if (res['ud_priority'] != taskarg['ud_priority']):
        adj_priority = Decimal(taskarg['ud_priority'])
    else:
        adj_priority = res['adj_priority']

    task.put_item(
        Item={
            'username': username,
            'task_id': task_id,
            'created': res['created'],
            'modified': datetime.utcnow().isoformat(),
            'finished': datetime.utcnow().isoformat(),
            'comp_time': 0,
            'adj_priority': adj_priority,
            'ud_priority': taskarg['ud_priority'],
            'ud_time': Decimal(taskarg['ud_time']),
            'deadline': taskarg['deadline'],
            'item': taskarg['item'],
            'description': taskarg['description']
        }
    )
    return


def _task_delete(username, task_id):
    task.delete_item(
        Key={
            'username': username,
            'task_id': task_id
        }
    )
    return


    


def task_update_priority(username, task_id, higher_task_id=0, lower_task_id=0):
    if higher_task_id:
        higher = task_get(username, higher_task_id)['adj_priority']
    else:
        higher = 5

    if lower_task_id:
        lower = task_get(username, lower_task_id)['adj_priority']
    else:
        lower = 0

    response = task.get_item(
        Key={
            'username': username,
            'task_id': task_id
        }
    )
    res = response['Item']

    adj_priority = (higher + lower) / 2

    task.put_item(
        Item={
            'username': username,
            'task_id': task_id,
            'created': res['created'],
            'modified': datetime.utcnow().isoformat(),
            'finished': datetime.utcnow().isoformat(),
            'comp_time': 0,
            'adj_priority': adj_priority,
            'ud_priority': res['ud_priority'],
            'ud_time': res['ud_time'],
            'deadline': res['deadline'],
            'item': res['item'],
            'description': res['description']
        }
    )


def _task_close(username, task_id, completed_time):
    task.update_item(
        Key={
            'username': username,
            'task_id': int(task_id)
        },
        UpdateExpression='SET finished = :val1, comp_time = :val2',
        ExpressionAttributeValues={
            ':val1': datetime.utcnow().isoformat(),
            ':val2': Decimal(completed_time),
        }
    )
    return


def _tasksarchive_update_remove_task(username, task_id):
    response = tasksarchive.get_item(
        Key={
            'username': username,
        }
    )
    res = response['Item']

    task_list = res['tasks']
    task_list.remove(task_id)

    tasksarchive.update_item(
        Key={
            'username': username,
        },
        UpdateExpression='SET tasks = :val1',
        ExpressionAttributeValues={
            ':val1': task_list
        }
    )
    return


def _taskarchive_update_add_task(username, task_id):
    # Returns the task_id that should be added.  Ensures tasks are added sequentially.s
    response = tasksarchive.get_item(
        Key={
            'username': username,
        }
    )
    res = response['Item']
    task_list = res['tasks']
    if len(task_list) == 0:
        task_list = [task_id]
    else:
        task_list.append(task_id)

    tasksarchive.update_item(
        Key={
            'username': username,
        },
        UpdateExpression='SET tasks = :val1',
        ExpressionAttributeValues={
            ':val1': task_list
        }
    )
    return


def task_remove(username, task_id):
    try:
        _tasks_update_remove_task(username, task_id)
    except:
        _tasksarchive_update_remove_task(username, task_id)
    _task_delete(username, task_id)
    return


def task_archive(username, task_id, completed_time):
    _tasks_update_remove_task(username, task_id)
    _taskarchive_update_add_task(username, task_id)
    _task_close(username, task_id, completed_time)
    return


def task_blowup(username, task_id, ntasks=4):
    weight = .01
    task_id = Decimal(task_id)
    parent = task_get(username, task_id)
    if not parent:
        print "Empty parent"
        return []
    task_remove(username, task_id)
    task_id_list = []
    for i in range(ntasks):
        task_id = _tasks_update_new_task(username)
        offset = weight * ((ntasks - 1 - i) + random.random())
        # print(offset)
        task.put_item(
            Item={
                'username': username,
                'task_id': task_id,
                'created': parent['created'],
                'modified': datetime.utcnow().isoformat(),
                'finished': datetime.utcnow().isoformat(),
                'comp_time': 0,
                'adj_priority': Decimal(parent['ud_priority']) + Decimal(offset),
                'ud_priority': parent['ud_priority'],
                'ud_time': Decimal(parent['ud_time'] / ntasks),
                'deadline': parent['deadline'],
                'item': parent['item'] + ' - Part '+str(i+1),
                'description': parent['description']
            }
        )
        task_id_list.append(task_id)
        
        
    return _tasks_batch(username, task_id_list)


def _tasks_batch(username, task_id_list = []):
    print task_id_list
    if not task_id_list: # I wasn't passed a list
        task_id_list = tasks_get(username)['tasks']
        if not task_id_list: # A list doesn't exist.
            return []
    
    
    key_list = [];
    for task_id in task_id_list:
        key_term = {'username': username, 'task_id': int(task_id)}
        key_list.append(key_term)
    response = dynamodb.batch_get_item(
        RequestItems={
            'task': {
                'Keys': key_list,
            }
        }
    )

    tasks = response['Responses']['task']
    return sorted(tasks, key=lambda task: task['adj_priority'], reverse=True)


def tasks_list(username, nitems=0):
    tasks = _tasks_batch(username)
    if nitems == 0 or nitems > len(tasks):
        return tasks
    else:
        return tasks[0:nitems]


def taskarchive_get(username):
    response = tasksarchive.get_item(
        Key={
            'username': username,
        }
    )
    return response['Item']


def new_priority(task_num, num_tasks):
    MAX_PRIORITY = 4.9
    MIN_PRIORITY = 0.1

    priority_step = (MAX_PRIORITY-MIN_PRIORITY)/(num_tasks+1)
    return Decimal(MIN_PRIORITY + (num_tasks - task_num) * priority_step)
    
    
def task_update_all_priority(username, task_id_list):
    if not task_id_list:
        return
    tasks = tasks_list(username)

    num_tasks = len(tasks)
    put_requests = []
    
    for task in tasks:
        task_num = task_id_list.index(task['task_id'])
        #print task_num
        put_request =  {
            'PutRequest': {
                'Item': {
                    'username': task['username'],
                    'task_id': task['task_id'],
                    'created': task['created'],
                    'modified': datetime.utcnow().isoformat(),
                    'finished': datetime.utcnow().isoformat(),
                    'comp_time': task['comp_time'],
                    'adj_priority': new_priority(task_num, num_tasks),
                    'ud_priority': task['ud_priority'],
                    'ud_time': task['ud_time'],
                    'deadline': task['deadline'],
                    'item': task['item'],
                    'description': task['description']
                }
            }   
        }
        #print put_request['PutRequest']['Item']['task_id']
        #print put_request['PutRequest']['Item']['adj_priority']
        put_requests.append(put_request)
        
    response = dynamodb.batch_write_item(
        RequestItems={
            'task': put_requests
        }
    )
