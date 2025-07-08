"""
test for ai-agent project
"""

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


class TestGetFilesFunction(unittest.TestCase):
    """Test methods for get_files_info function"""

    def test_current_folder(self):
        result = get_files_info("calculator", ".")
        print(result)
        self.assertEqual("pkg: file_size=" in result, True)

    def test_pkg_folder(self):
        result = get_files_info("calculator", "pkg")
        print(result)
        self.assertEqual("calculator.py: file_size=" in result, True)

    def test_not_directory(self):
        result = get_files_info("calculator", "pkg/calculator.py")
        print(result)
        self.assertEqual(result, 'Error: "pkg/calculator.py" is not a directory')

    def test_bin_folder(self):
        result = get_files_info("calculator", "/bin")
        print(result)
        self.assertEqual(
            result,
            'Error: Cannot list "/bin" as it is outside the permitted working directory',
        )

    def test_outside_folder(self):
        result = get_files_info("calculator", "../")
        print(result)
        self.assertEqual(
            result,
            'Error: Cannot list "../" as it is outside the permitted working directory',
        )


class TestFileContentFunction(unittest.TestCase):
    """Test methods for get_files_info function"""

    def test_calculator_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        self.assertEqual("def main():" in result, True)

    def test_pkg(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertEqual("class Calculator:" in result, True)

    def test_not_file(self):
        result = get_file_content("calculator", "pkg/")
        print(result)
        self.assertEqual(
            result, 'Error: File not found or is not a regular file: "pkg/"'
        )

    def test_outside_folder(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertEqual(
            result,
            'Error: Cannot read "/bin/cat" as it is outside the permitted working directory',
        )


if __name__ == "__main__":
    unittest.main()
