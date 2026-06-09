# test_io_utils.py - Tests for methods in the IOManager class.

import unittest

from scripts._red.io_manager import IOManager
from resources.resource_dir import Resource

IOM: IOManager = IOManager()

EXPECTED_YAML_RESULT: dict = {"greet": {"en": ["hello", "heya", "hi"]}}
EXPECTED_TOML_RESULT: dict = {"greet": {"es": "hola"}}
EXPECTED_JSON_RESULT: dict = {"greet": {"de": "wilkommen"}}
EXPECTED_TEXT_RESULT: str = "{greet: {jp: [ohayo gozaimasu, konnichiwa, konbanwa]}}"
READ_TEST_FILE: str = "tests/_red/io_utils_read_test"
YAML_FILE_TYPES: list[str] = [".yaml", ".yml"]
TOML_FILE_TYPES: list[str] = [".toml"]
JSON_FILE_TYPES: list[str] = [".json"]
TEXT_FILE_TYPES: list[str] = [".text", ".txt"]

WRITE_TEST_CONTENTS: dict = {"goodbye": {"de": "tschuss"}}
WRITE_TO_YAML_DIR: str = "tests/_red/"
WRITE_TO_YAML_FILE: str = "io_utils_write_test.yaml"
WRITE_TO_YAML_PATH: str = WRITE_TO_YAML_DIR + WRITE_TO_YAML_FILE


class TestIOUtils(unittest.TestCase):

    def test_read_files(self):
        print(f"\nSetting up tests for reading files...")
        print(f"Set up complete\n")

        print(f"Testing reading YAML files")
        for file_type in YAML_FILE_TYPES:
            filepath = READ_TEST_FILE + file_type
            self.assertEqual(EXPECTED_YAML_RESULT, IOM.read_file(filepath=filepath))
            self.assertEqual(EXPECTED_YAML_RESULT, IOM._read_yaml(filepath=filepath))
        print(f"Test case passed!\n")

        print(f"Testing reading TOML files")
        for file_type in TOML_FILE_TYPES:
            filepath = READ_TEST_FILE + file_type
            self.assertEqual(EXPECTED_TOML_RESULT, IOM.read_file(filepath=filepath))
            self.assertEqual(EXPECTED_TOML_RESULT, IOM._read_toml(filepath=filepath))
        print(f"Test case passed!\n")

        print(f"Testing reading JSON files")
        for file_type in JSON_FILE_TYPES:
            filepath = READ_TEST_FILE + file_type
            self.assertEqual(EXPECTED_JSON_RESULT, IOM.read_file(filepath=filepath))
            self.assertEqual(EXPECTED_JSON_RESULT, IOM._read_json(filepath=filepath))
        print(f"Test case passed!\n")

        print(f"Testing reading TEXT files")
        for file_type in TEXT_FILE_TYPES:
            filepath = READ_TEST_FILE + file_type
            self.assertEqual(EXPECTED_TEXT_RESULT, IOM.read_file(filepath=filepath))
            self.assertEqual(EXPECTED_TEXT_RESULT, IOM._read_text(filepath=filepath))
        print(f"Test case passed!\n")

        print(f"Tests for reading files all passed!\n")

    def test_write_file(self):
        print(f"\nSetting up tests for writing files...")
        print(f"Set up complete\n")

        print(f"Testing writing a file")
        assert IOM._write_file(filepath=WRITE_TO_YAML_PATH, data=WRITE_TEST_CONTENTS)
        self.assertEqual(WRITE_TEST_CONTENTS, IOM.read_file(filepath=WRITE_TO_YAML_PATH))
        print(f"Test case passed!\n")
        
        print(f"Tests for reading files all passed!\n")

    def test_load_a_save_file(self):
        print(f"\nSetting up tests for loading save files...")
        print(f"Set up complete\n")

        print(f"Testing differentiating between valid and invalid saves")
        expected_valid_saves = ["test"]
        expected_invalid_saves = ["Day"]
        self.assertEqual((expected_valid_saves, expected_invalid_saves),
                         IOM.get_valid_save_names())
        print(f"Test case passed!\n")

        print(f"Testing loading the camp save file")
        IOM.read_camp_save_file()
        print(f"Test case passed!\n")

        print(f"Testing ")
        print(f"Test case passed!\n")

        print(f"Testing ")
        print(f"Test case passed!\n")

        print(f"Tests for loading a save file all passed!\n")


if __name__ == '__main__':
    unittest.main()
