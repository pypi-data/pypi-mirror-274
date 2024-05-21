# tests/test_utils.py

from unittest import TestCase
from hyperdyn.utils import create_directory, copy_file, get_config_path
import os
import shutil

class TestUtils(TestCase):
    def test_create_directory(self):
        # Arrange
        directory_path = "tests/temp_directory"

        # Act
        create_directory(directory_path)

        # Assert
        self.assertTrue(os.path.exists(directory_path))
        self.addCleanup(shutil.rmtree, directory_path)

    def test_copy_file(self):
        # Arrange
        source_file = "tests/data/source_file.txt"
        destination_dir = "tests/temp_directory"
        expected_copied_file = os.path.join(destination_dir, "source_file.txt")

        # Act
        copy_file(source_file, destination_dir)

        # Assert
        self.assertTrue(os.path.exists(expected_copied_file))
        self.addCleanup(shutil.rmtree, destination_dir)

    def test_get_config_path(self):
        # Arrange
        expected_config_path = os.path.expanduser("~/.hyperdyn/config.ini")

        # Act
        config_path = get_config_path()

        # Assert
        self.assertEqual(config_path, expected_config_path)
