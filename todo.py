#!/usr/bin/env python3
import argparse
from argparse import RawTextHelpFormatter
from models.task import Task
# import sys
import models
from datetime import datetime


# Add task command
def add_task(args):
    """
    Adds a new task to the todo list.
    Args:
        args: An object containing the task details,
        specifically the 'title' attribute.
    Side Effects:
        - Creates a new Task instance with the provided title.
        - Saves the task to persistent storage.
        - Prints a confirmation message with the task title and its unique ID.
    """
    
    task = str(args.title)
    if args.duedate and args.duetime:
        combined = f"{args.duedate} {args.duetime}"
        duedatetime = datetime.strptime(combined, "%Y-%m-%d %H:%M")
    else:
        duedatetime = None
    
    if args.urgent:
        priority = "urgent"
    else:
        priority = 'not urgent'

    add_task = Task(
        task,
        duedatetime=duedatetime,
        priority=priority
    )
    add_task.save()
    print(
        f"✅ Task added {'[Urgent]' if args.urgent else ''}: {args.title}"
        f"{(
        f'\n\tDue: {args.duedate} at {args.duetime}' 
            if args.duedate and args.duetime else ''
        )}"
        f"\n\nTask ID: {add_task.id}"
    )

# List task command
def list_tasks(args):
    if args.completed:
        print("\n📋 Task List:")
        data = Task.print_completed_task()
        print(data)
    else:
        print("\n📋 Task List:")
        data = Task.print_tasks()
        print(data)

#Complete 
def complete_task(args):
    message = Task.mark_complete(args.id)
    print(message)

def delete_task(args):
    task_id = str(args.id)
    result = Task.remove_task(task_id)
    print(result)

def edit_task(args):
    print(f'Editted task {args.id}')
    all_tasks = models.store.all()
    for key, value in all_tasks.items():
        get_id = key.split('.')[1]
        if get_id == args.id:
            if args.urgent:
                value.priority = 'urgent'
            elif args.not_urgent:
                value.priority = 'not urgent'
            value.title = args.title
    models.store.save()

parser = argparse.ArgumentParser(
    description='Advanced TODO CLI'
)
subparsers = parser.add_subparsers(
    title='Commands',
    dest="command"
)

# Add command
add_parser = subparsers.add_parser(
    "add",
    usage="./todo.py add \"<task title>\"",
    help="Add a new task",
    description=(
        "Add a new task to your TODO list.\n\n"
        "This command lets you create a new task by specifying its title.\n"
        "If the title is more than one word, enclose it in quotes."
    ),
    epilog=(
        "Examples:\n"
        "  - If just one word, you can do:\n"
        "    ./todo.py add groceries\n\n"
        "  - Else:\n"
        "    ./todo.py add \"Buy groceries\"\n"
        "    ./todo.py add \"Call the dentist\"\n"
        "    ./todo.py add \"Finish ALX project by 5pm\"\n"
    ),
    formatter_class=RawTextHelpFormatter
)
add_parser.add_argument('title', help='Title of the task')
add_parser.add_argument('--duedate', help="Add date for task to be done")
add_parser.add_argument('--duetime', help="Add time of the day for task to be done")
add_parser.add_argument('--urgent', action='store_true', help="Add priority to task")
add_parser.set_defaults(func=add_task)

# List command 
list_parser = subparsers.add_parser(
    'list',
    help='List tasks in your TODO list',
    usage="./todo.py list [--completed]",
    description=(
        "List all tasks in your TODO list.\n\n"
        "By default, it shows all tasks (both completed and pending).\n"
        "Use the optional --completed flag to filter"
        " and show only completed tasks."
    ),
    epilog=(
        "Examples:\n"
        "  - List all tasks:\n"
        "    ./todo.py list\n\n"
        "  - List only completed tasks:\n"
        "    ./todo.py list --completed\n"
    ),
    formatter_class=argparse.RawTextHelpFormatter
)
list_parser.add_argument(
    '--completed',
    action='store_true',
    help='Show only completed tasks'
)
list_parser.set_defaults(func=list_tasks)

# Mark a task as completed.
mark_complete_parser = subparsers.add_parser(
    "complete",
    help="Change status of a task",
    description=(
        "Mark a Task as completed"
    ),
    epilog=(
        "\nExample:\n"
        "\t./todo.py complete <ID>"
    ),
    formatter_class=argparse.RawTextHelpFormatter
)
mark_complete_parser.add_argument("id", type=str, help="ID of the task to remove")
mark_complete_parser.set_defaults(func=complete_task)

# Delete Task command
remove_parser = subparsers.add_parser("delete", help="Remove a task")
remove_parser.add_argument("id", help="ID of the task to remove")
remove_parser.set_defaults(func=delete_task)

# Edit Task
edit_parser = subparsers.add_parser(
    'edit',
    help='Edit a task by providing Task\'s ID'
)
edit_parser.add_argument('id', help='ID of the task you intend to edit')
edit_parser.add_argument(
    '--urgent',
    action='store_true',
    help='Add priority to a task'
)
edit_parser.add_argument(
    '--title',
    help='Edit title of a task'
)
edit_parser.add_argument(
    '--not-urgent',
    action='store_true',
    help='Edit priority of a task'
)
edit_parser.set_defaults(func=edit_task)


args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()