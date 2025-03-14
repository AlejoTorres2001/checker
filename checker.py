
from enum import Enum
import os
import sys
import json
import io
import re
import importlib.util
import unittest
from unittest.mock import patch
from dotenv import load_dotenv
import requests
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from utils.consignas import EJOB_1_B 

UTEST_DIR = "tests"
UTEST_FILENAME = "ejB.test.py"
EXAMS_DIR = "parciales"
ASSIGNMENT = EJOB_1_B


load_dotenv()


class TestResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"


class JSONTestResult(unittest.TestResult):
    """A custom TestResult class that collects test results in JSON format.

    This class extends unittest.TestResult to store test execution results in a structured JSON format.
    Each test result includes the test name, description, result status (PASSED, FAILED, ERROR),
    and a reason or error message.

    Attributes:
      results (list): A list of dictionaries containing the test results.
      result_options (TestResult): An enum containing the possible test result statuses.

    Methods:
      addSuccess(test): Records a successful test execution.
      addFailure(test, err): Records a test failure.
      addError(test, err): Records a test error.

    Each result dictionary contains:
      - test: The name of the test method
      - description: The test's description (from docstring)
      - result: The test result status (PASSED/FAILED/ERROR)
      - reason: Explanation of the result or error message
    """

    def __init__(self, *args, **kwargs):
        super(JSONTestResult, self).__init__(*args, **kwargs)
        self.results = []
        self.result_options = TestResult

    def addSuccess(self, test):
        description = test.shortDescription() or ""
        self.results.append({
            "test": test._testMethodName,
            "description": description,
            "result": self.result_options.PASSED.value,
            "reason": "Test passed successfully"
        })
        super(JSONTestResult, self).addSuccess(test)

    def addFailure(self, test, err):
        description = test.shortDescription() or ""
        reason = self._exc_info_to_string(err, test)
        self.results.append({
            "test": test._testMethodName,
            "description": description,
            "result": self.result_options.FAILED.value,
            "reason": reason
        })
        super(JSONTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        description = test.shortDescription() or ""
        reason = self._exc_info_to_string(err, test)
        self.results.append({
            "test": test._testMethodName,
            "description": description,
            "result": self.result_options.ERROR.value,
            "reason": reason
        })
        super(JSONTestResult, self).addError(test, err)


def load_module_from_path(module_name, module_path):
    """
    Loads a Python module from a given file path.

    This function dynamically imports a Python module from a specified file path using the importlib
    utility. It creates a module specification, loads the module, and executes it.

    Args:
      module_name (str): The name to be given to the loaded module
      module_path (str): The file path where the module is located

    Returns:
      module: The loaded Python module object

    Raises:
      ImportError: If the module cannot be loaded
      AttributeError: If the module does not contain expected attributes
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_test_module_from_path(module_name, module_path):
    """
    Dynamically loads a test module from a given file path with special handling for exam function imports.
    This function reads a Python test file and modifies how exam functions are imported by wrapping
    each import in a try/except block. This allows for graceful handling of missing functions.
    Args:
      module_name (str): The name to give to the loaded module
      module_path (str): The file path to the test module to load
    Returns:
      module: The loaded test module object with modified imports
    Raises:
      FileNotFoundError: If the specified module_path does not exist
      SyntaxError: If the source code in the file has syntax errors
    Example:
      >>> test_module = load_test_module_from_path("test_exam", "./test_exam.py")
      >>> test_module.some_test_function()
    Note:
      The function specifically looks for and modifies imports in the format:
      'from exam import function1, function2, ...'
    """
    with open(module_path, "r") as f:
        test_source = f.read()
    pattern = r"^from\s+exam\s+import\s+(.+)$"
    match = re.search(pattern, test_source, re.MULTILINE)
    if match:
        imported_functions = match.group(1)
        func_list = [fn.strip() for fn in imported_functions.split(",")]
        #!Generate try/except blocks for each function import
        replacement = ""
        for fn in func_list:
            replacement += f"try:\n    from exam import {fn}\n"
            replacement += f"except ImportError as e:\n"
            replacement += f"    def {fn}(*args, **kwargs):\n"
            replacement += f"        raise ImportError('Function \"{fn}\" not found. ' + str(e))\n"
        test_source = re.sub(pattern, replacement,
                             test_source, count=1, flags=re.MULTILINE)
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    test_module = importlib.util.module_from_spec(spec)
    exec(test_source, test_module.__dict__)
    return test_module


def run_tests_for_student(student_module_path, test_module_path, assignment):
    """
    Runs unit tests for a student's module against a test module and returns the test results.

    This function attempts to load a student's Python module and a corresponding test module,
    then executes all tests found in the test module against the student's code. The function

    Parameters:
    ----------
    student_module_path : str
      File path to the student's Python module to be tested
    test_module_path : str
      File path to the test module containing the unit tests

    Returns:
    -------
    list
      A list of dictionaries containing test results. Each dictionary has the following keys:
      - 'test': str, name of the test or error type
      - 'description': str, description of the test or error
      - 'result': str, test outcome ('passed' or 'failed')
      - 'reason': str, explanation of failure (if applicable)

    Possible Error Returns:
    --------------------
    - ModuleLoadError: When student's module fails to load
    - TestModuleLoadError: When test module fails to load
    - TestExecutionError: When an error occurs during test execution

    Notes:
    -----
    The function uses JSONTestResult class for formatting test results
    and temporarily registers the student's module in sys.modules as "exam" to allow proper importing.
    """
    try:
        student_module = load_module_from_path("exam", student_module_path)
        # ! makes  "from exam import ..." work in test_module
        sys.modules["exam"] = student_module
    except Exception as e:
        return [{
            "test": "ModuleLoadError",
            "description": "El módulo del estudiante no pudo cargarse",
            "result": "failed",
            "reason": str(e)
        }]
    try:
        #! Load modify test module
        test_module = load_test_module_from_path(
            "exam_test_module", test_module_path)
    except Exception as e:
        return [{
            "test": "TestModuleLoadError",
            "description": "El módulo de tests no pudo cargarse",
            "result": "failed",
            "reason": str(e)
        }]
    try:
        #! run all tests
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
        stream = io.StringIO()
        runner = unittest.TextTestRunner(
            stream=stream, resultclass=JSONTestResult, verbosity=2)
        result = runner.run(suite)

        # Read student's source code
        with open(student_module_path, 'r') as f:
            student_code = f.read()

        # Read test source code
        with open(test_module_path, 'r') as f:
            test_code = f.read()

        # Add source codes to results
        return {
            "results": result.results,
            "exam": student_code,
            "testCode": test_code,
            "assignment": assignment
        }
    except Exception as e:
        return [{
            "test": "TestExecutionError",
            "description": "Error durante la ejecución de los tests",
            "result": "failed",
            "reason": str(e)
        }]


def main_runner(exams_dir, utest_dir, utest_filename, assignment) -> str:
    """
    Executes unit tests for Python scripts in a specified directory and collects results.
    This function processes Python files in the EXAMS_DIR directory, running unit tests
    defined in UTEST_DIR/UTEST_FILENAME against each student's submission. Results are
    collected and returned as a JSON formatted output.
    Returns:
      JSON-formatted dictionary where:
        - Keys are student names (derived from filenames without extension)
        - Values are test results for each student's submission
    Example of output format:
      {
        "student1": {test_results},
        "student2": {test_results},
        ...
      }
    Notes:
      - Assumes student's name is the filename without extension
      - Expects test module in UTEST_DIR/UTEST_FILENAME
      - Skips non-Python files in EXAMS_DIR
    """
    final_results = {}
    test_module_path = os.path.join(utest_dir, utest_filename)

    if not os.path.isdir(exams_dir):
        print("Exams directory not found")
        return ""

    #! Loop over exams files - requires format studentname.py
    python_files = [file for file in os.listdir(
        exams_dir) if file.endswith(".py")]

    print(f"Found {len(python_files)} valid python files...")
    for i, file in enumerate(python_files, 1):
        student_module_path = os.path.join(exams_dir, file)
        student_name = os.path.splitext(file)[0]
        print(
            f"[{i}/{len(python_files)}] Running tests for student: {student_name}", file=sys.stderr)
        test_output = run_tests_for_student(
            student_module_path, test_module_path, assignment)
        print(f"✓ Completed tests for: {student_name}", file=sys.stderr)

        if isinstance(test_output, list):  # Error case
            final_results[student_name] = {
                "results": test_output,
                "exam": "",
                "testCode": "",
                "assignment": assignment
            }
        else:  # Success case
            final_results[student_name] = test_output
    print("All tests completed.")
    return json.dumps(final_results, indent=4)


if __name__ == "__main__":
    os.makedirs("informes", exist_ok=True)
    json_results = main_runner(exams_dir=EXAMS_DIR, utest_dir=UTEST_DIR,
                               utest_filename=UTEST_FILENAME, assignment=ASSIGNMENT)

    try:
        parsed_json = json.loads(json_results)

        #!AI
        webhook_url = os.getenv("WEBHOOK_URL")
        webhook_secret = os.getenv("WEBHOOK_SECRET")
        response = requests.post(
            webhook_url,
            json=parsed_json,
            headers={
                'CheckerCredentials': webhook_secret,
                'Content-Type': 'application/json',
            }
        )

        response.raise_for_status()

        response_data = response.json()

        # Process each item in the response data
        if "data" in response_data:
            for item in response_data["data"]:
                # Format source code to be more readable
                if "exam" in item:
                    item["exam"] = item["exam"].encode().decode(
                        "unicode_escape")
                if "testCode" in item:
                    item["testCode"] = item["testCode"].encode().decode(
                        "unicode_escape")

                # Format test results to be more readable
                for test in item.get("results", []):
                    if "reason" in test:
                        test["reason"] = test["reason"].encode().decode(
                            "unicode_escape")

        # Save formatted JSON response
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"informes/results_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=4, ensure_ascii=False)

        print(f"Results saved to:")
        print(f"- JSON: {json_filename}")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request to webhook: {e}")
    except Exception as e:
        print(f"Error saving results: {e}")
