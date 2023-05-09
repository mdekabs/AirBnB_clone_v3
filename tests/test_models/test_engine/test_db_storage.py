#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        database = DBStorage()
        """Start a session"""
        database.reload()

        """Generate data"""
        for value in classes.values():
            instance = value()
            database.new(instance)

        data = database.all()
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                self.assertIn(value.__name__, data)
        """End session"""
        database.close()

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_all_wit_class(self):
        """Test that all returns all rows when class is passed"""
        database = DBStorage()
        """Start a session"""
        database.reload()

        """Generate data"""
        for value in classes.values():
            instance = value()
            database.new(instance)

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                data = database.all(value)
                self.assertIn(value.__name__, data)
        """End session"""
        database.close()

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        database = DBStorage()
        """Start a session"""
        database.reload()

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                inst = value()
                """Get the initial number of obj before add"""
                num = len(database.all())
                """Place the data in database.__session"""
                database.new(inst)
                """Get the number of object after new"""
                after_num = len(database.all())
                self.assertNotEqual(num, after_num)
        """End session"""
        database.close()

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        database = DBStorage()
        """Start a session"""
        database.reload()
        """Get the number of object in the database"""
        num = len(database.all())

        """Generate data"""
        for value in classes.values():
            instance = value()
            database.new(instance)

        """Save the data """
        database.save()

        """close the session"""
        database.close()

        """Start another session to get the data form the database"""
        database.reload()
        """Get the number of object in the database"""
        num_aftr_save = len(database.all())

        self.assertNotEqual(num, num_aftr_save)

        """close the session"""
        database.close()

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_get(self):
        """Test that get properly fetch the object"""
        database = DBStorage()
        """Start a session"""
        database.reload()
        """Create an instance to test"""
        instance = State(name="Lagos")

        database.new(instance)

        id = instance.id
        get_obj = database.get(State, id)

        self.assertEqual(id, get_obj.id)
        self.assertIsInstance(get_obj, State)
        self.assetEqual(type(id), str)

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_count(self):
        """Test that count properly return the number of objects."""
        database = DBStorage()
        """Start a session"""
        database.reload()

        """Generate data"""
        for value in classes.values():
            instance = value()
            database.new(instance)

        """Test if not cls was passed """
        no_cls = len(database.all())
        test_no_cls = database.count()
        self.assertEqual(no_cls, test_no_cls)

        """Test when cls is present"""
        for value in classes.values():
            with self.subTest(value=value):
                cls_cnt = len(database.all(value))
                test_cls = database.count(value)
                self.assertEqual(cls_cnt, test_cls)
        """End the session"""
        database.close()
