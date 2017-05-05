import boto3
from taskpop import dynamo
import pprint

username = "lars@gmail.com"

def lambda_logic():
    # assume callback says the username

    ntasks = 15
    max_items = 50

    # Setup boto3 resources
    dynamodb = boto3.resource('dynamodb')
    tasks_table = dynamodb.Table('tasks')
    tasksarchive_table = dynamodb.Table('tasksarchive')

    # Get the task list from tasksarchive
    response = tasksarchive_table.get_item(
        Key={
            'username': username,
        }
    )
    task_id_list = response['Item']['tasks']
    task_id_list.reverse() # should be oldest first
    if len(task_id_list) > max_items:
        task_id_list = task_id_list[0:max_items]
    
    # Batch get the items    
    key_list = [];
    for task_id in task_id_list:
        key_term = {'username': username, 'task_id': task_id}
        key_list.append(key_term)
        
    response = dynamodb.batch_get_item(
        RequestItems={
            'task': {
                'Keys': key_list,
            }
        }
    )
    tasks = response['Responses']['task']

    # Sort to get the ntasks most recent completed tasks
    tasks = sorted(tasks, key=lambda task: task['finished'], reverse=True)
    if len(tasks) > ntasks:
        tasks = tasks[0:ntasks]
        
    # Calculate the multiplier
    actual_time = 0
    estimated_time = 0
    for task in tasks:
        actual_time = task['comp_time'] + actual_time
        estimated_time = task['ud_time'] + estimated_time
    multiplier = actual_time / estimated_time

    # Update the multiplier
    tasks_table.update_item(
        Key={
            'username': username,
        },
        UpdateExpression='SET multiplier = :val1',
        ExpressionAttributeValues={
            ':val1': multiplier
        }
    )
    return multiplier


def test_lambda_logic():
    multiplier = lambda_logic()
    print(multiplier)
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(dynamo.tasks_get(username))
    
test_lambda_logic()
