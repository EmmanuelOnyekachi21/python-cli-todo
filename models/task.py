#!/usr/bin/env python3
"""
task.py
"""
from models.base_model import BaseModel
from datetime import datetime


class Task(BaseModel):
    """
    Represents a task in the todo list.
    """
    def __init__(
        self, title, status='pending',
        project_name=None, duedatetime=None, priority=None, completed_at=None
    ):
        """
        Initializes a new Task instance.
        """
        super().__init__()
        self.title = title
        self.status = status
        self.project_name = project_name
        self.priority = priority
        self.duedatetime = duedatetime
        self.completed_at = completed_at

    def __str__(self):
        """
        Returns a string representation of the Task instance.

        Returns:
            str: A string in the format
            '[Task] (<id>) <attribute dictionary>'
        """
        return f'[Task] ({self.id}) {self.__dict__}'

    def mark_completed(self):
        """
        Marks the task as completed by updating its status and
        setting the completed_at timestamp.
        """
        self.status = "completed"
        self.updated_at = datetime.now()
        self.completed_at = datetime.now()

    def mark_pending(self):
        """
        Marks the task as pending by updating its status and
        clearing the completed_at timestamp.
        """
        self.status = "pending"
        self.completed_at = None
        self.updated_at = datetime.now()
