"""
test for ai-agent project
"""

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


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

class TestWriteFileFunction(unittest.TestCase):

    def test_succesfully(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)

    def test_succesfully2(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)

    def test_outside_failure(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)


class TestRunPythonFunction(unittest.TestCase):

    def test_succesfully(self):
        result = run_python_file("calculator", "main.py")
        print(result)

    def test_nonexists(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)

    def test_outside_failure(self):
        result = run_python_file("calculator", "../main.py")
        print(result)
    
    def test_run_calculator(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)


if __name__ == "__main__":
    unittest.main()
