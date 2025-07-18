"""
This module contains unit tests for the Task Class
"""
import unittest
from models.task import Task
from datetime import datetime, timedelta


class TestTask(unittest.TestCase):
    """
    Test the Task Class.
    """
    def setUp(self):
        """
        Sets up a new Task instance for testing.
        """
        self.due = datetime.now() + timedelta(days=1)
        self.task = Task(
            title="Test Task",
            status="pending",
            project_name="Test Project",
            duedatetime=datetime(2023, 10, 1, 12, 0),
            priority="high"
        )

    def tearDown(self):
        """
        Tears down the Task instance after each test.
        """
        del self.task
        del self.due

    def test_inheritance(self):
        """
        Test that Task properly inheriited from BaseModel
        and has certain fields.
        """
        self.assertTrue(hasattr(self.task, 'id'))
        self.assertTrue(hasattr(self.task, 'created_at'))
        self.assertTrue(hasattr(self.task, 'updated_at'))

    def test_initialization(self):
        """
        Tests the initialization of Task to ensure it sets
        the attributes correctly.
        """
        self.assertIsInstance(self.task, Task)
        self.assertIsInstance(self.task.id, str)
        self.assertIsInstance(self.task.title, str)
        self.assertIsInstance(self.task.status, str)
        self.assertIsInstance(self.task.project_name, str)
        self.assertIsInstance(self.task.duedatetime, datetime)
        self.assertIsInstance(self.task.priority, str)
        self.assertIsNone(self.task.completed_at)
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.priority, "high")

    def test_str_method(self):
        """
        Tests the __str__ method of Task to ensure it returns
        the correct string representation.
        """
        expected_str = f"[Task] ({self.task.id}) {self.task.__dict__}"
        self.assertEqual(str(self.task), expected_str)

    def test_mark_completed(self):
        """
        Tests the mark_completed method to ensure it updates
        the status and completed_at attributes correctly.
        """
        self.task.mark_completed()
        self.assertEqual(self.task.status, "completed")
        self.assertIsInstance(self.task.completed_at, datetime)
        self.assertIsInstance(self.task.updated_at, datetime)

    def test_mark_pending(self):
        """
        Test the mark_pending method to ensure it updates its status
        """
        self.task.mark_completed()  # first complete it
        self.task.mark_pending()  # now go back
        self.assertEqual(self.task.status, "pending")
        self.assertIsNone(self.task.completed_at)
        self.assertIsInstance(self.task.updated_at, datetime)

    def test_updated_at_changes(self):
        before = self.task.updated_at
        self.task.mark_completed()
        after = self.task.updated_at
        self.assertNotEqual(before, after)
        self.assertTrue(after > before)

    def test_optional_fields(self):
        minimal_task = Task(title="Quick task", duedatetime=self.due)
        self.assertIsNone(minimal_task.project_name)
        self.assertIsNone(minimal_task.priority)

    def test_to_dict(self):
        """
        Tests the to_dict method inherited from BaseModel to ensure
        it returns a
        dictionary with the correct structure and types.
        """
        model_dict = self.task.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'Task')
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)

    def test_from_dict(self):
        obj = self.task.from_dict(self.task.to_dict())
        self.assertIsInstance(obj, Task)
