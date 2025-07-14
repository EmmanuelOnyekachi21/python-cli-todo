"""
This module contains unit tests for the BaseModel class.
"""
import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """
    Test the BaseModel class.
    """
    def setUp(self):
        """
        Sets up a new BaseModel instance for testing.
        """
        self.myModel = BaseModel()

    def tearDown(self):
        """
        Tears down the BaseModel instance after each test.
        """
        del self.myModel

    def test_initialization(self):
        """
        Tests the initialization of BaseModel to ensure it sets
        the id, created_at, and updated_at attributes correctly.
        """
        self.assertIsInstance(self.myModel, BaseModel)
        self.assertIsInstance(self.myModel.id, str)
        self.assertIsInstance(self.myModel.created_at, datetime)
        self.assertIsInstance(self.myModel.updated_at, datetime)

    def test_unique_ids(self):
        """
        Tests that each instance of BaseModel has a unique ID.
        """
        model = BaseModel()
        self.assertNotEqual(self.myModel.id, model.id)

    def test_to_dict(self):
        """
        Tests the to_dict method of BaseModel to ensure it returns a
        dictionary with the correct structure and types.
        """
        model_dict = self.myModel.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
