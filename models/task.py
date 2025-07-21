#!/usr/bin/env python3
"""
task.py
"""
from models.base_model import BaseModel
from datetime import datetime
import models
from tabulate import tabulate


class Task(BaseModel):
    """
    Represents a task in the todo list.
    """
    def __init__(
        self, title, status='pending',
        project_name=None, duedatetime=None, priority=None
    ):
        """
        Initializes a new Task instance.
        """
        self.title = title
        self.status = status
        self.project_name = project_name
        self.priority = priority
        self.duedatetime = duedatetime
        # self.completed = completed
        super().__init__()

    def __str__(self):
        """
        Returns a string representation of the Task instance.

        Returns:
            str: A string in the format
            '[Task] (<id>) <attribute dictionary>'
        """
        return f'[Task] ({self.id}) {self.__dict__}'

    def mark_pending(self):
        """
        Marks the task as pending by updating its status and
        clearing the completed_at timestamp.
        """
        self.status = "pending"
        self.completed_at = None
        self.updated_at = datetime.now()
    
    @staticmethod
    def print_tasks():
        """
        Retrieves and formats all tasks (completed or not) from the data store
        Iterates through all stored tasks, filters those with a status of
        includes the task ID, title, status, due date, and priority. If due date
        or priority is not set, 'None' is displayed for those fields.
        Returns:
            str: A formatted table of completed tasks using the 'github' style.
        """ 
        items = models.store.all()
        tasks = []
        for key, value in items.items():
            key = key.split('.')[1]
            dictionary = value.to_dict()
            dictionary['id'] = key
            tasks.append(
                dictionary
            )
        # print(tasks)
        # Build rows
        table = []
        
        for task in tasks:
            table.append([
                task['id'],
                task['title'],
                "✅ Completed" if task["status"].lower() == 'completed' else '❌ Pending',
                task['duedatetime'] if task['duedatetime'] else "None",
                task['priority'] if task['priority'] else 'None'
            ])
        headers = ['ID', 'Title', 'Status', 'Due Date', 'Priority']
        return (tabulate(table, headers=headers, tablefmt="github"))

    @staticmethod
    def print_completed_task():
        """
        Retrieves and formats all completed tasks from the data store.
        Iterates through all stored tasks, filters those with a status of
        includes the task ID, title, status, due date, and priority. If due date
        or priority is not set, 'None' is displayed for those fields.
        Returns:
            str: A formatted table of completed tasks using the 'github' style.
        """        
        items = models.store.all()
        tasks = []
        for key, value in items.items():
            key = key.split('.')[1]
            if value.status == 'completed':
                dictionary = value.to_dict()
                dictionary['id'] = key
                tasks.append(
                    dictionary
                )
        # print(tasks)
        # Build rows
        table = []
        
        for task in tasks:
            table.append([
                task['id'],
                task['title'],
                task["status"],
                task['duedatetime'] if task['duedatetime'] else "None",
                task['priority'] if task['priority'] else 'None'
            ])
        headers = ['ID', 'Title', 'Status', 'Due Date', 'Priority']
        return (tabulate(table, headers=headers, tablefmt="github"))


    @classmethod
    def mark_complete(cls, id):
        """
        Marks the task as completed by updating its status and
        setting the completed_at timestamp.
        """
        dictionary = models.store.all()
        key_id = f"{cls.__name__}.{id}"
        if key_id in dictionary:
            task = dictionary.get(key_id)
            if task.status == 'completed':
                return "✅ Task already completed"
            else:
                task.status = 'completed'
                task.save()
                return "🎉 Task marked as completed!"
        else:
            return "❌ Invalid Task ID"
            
        
