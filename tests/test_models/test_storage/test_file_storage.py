import unittest
import tempfile  # For creating temporary files
import os
import json

from models.task import Task
from models.storage.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        # Create Task object
        self.task = Task("Wash Plates")
        # create a temporary file for testing
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file.close()

        self.storage = FileStorage()
        self.storage._FileStorage__file_path = self.test_file.name  # Override file path
        FileStorage._FileStorage__objects = {}
    
    def tearDown(self):
        del self.task
        os.remove(self.test_file.name)
        FileStorage._FileStorage__objects = {}
    
    def test_new_and_all(self):
        self.storage.new(self.task)
        all_objects = self.storage.all()
        key = f"Task.{self.task.id}"
        self.assertIn(key, all_objects)
        self.assertIsInstance(all_objects, dict)
        self.assertIsInstance(all_objects[key], Task)

    # def test_save_creates_json_file(self):
    #     self.storage.new(self.task)
    #     self.storage.save()

    #     with open(self.test_file.name, 'r') as f:
    #         data = json.load(f)
        
    #     key = f"Task.{self.task.id}"
    #     self.assertIn(key, data)
    #     self.assertEqual(data[key]['title'], "Wash Plates")
    
    def test_reload_restores_objects(self):
        self.storage.new(self.task)
        self.storage.save()
        
        # Simulate restart
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        
        key = f"Task.{self.task.id}"
        all_objects = self.storage.all()

        self.assertIn(key, all_objects)
        self.assertIsInstance(all_objects[key], Task)
        self.assertEqual(all_objects[key].title, "Wash Plates")
    
    def test_delete_removes_object(self):
        self.storage.new(self.task)
        self.storage.delete(self.task)

        key = f"Task.{self.task.id}"
        self.assertNotIn(key, self.storage.all())
