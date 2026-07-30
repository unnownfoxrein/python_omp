import os
import subprocess

import pytest

SOLUTION_FOLDER_PATH = "solution"
RESOURCE_FOLDER_PATH = os.path.join("test", "resources", "task3")


@pytest.mark.parametrize(
    "test_input_file, expected_output_file",
    [
        (
            os.path.join(RESOURCE_FOLDER_PATH, "test_input_1.txt"),
            os.path.join(RESOURCE_FOLDER_PATH, "expected_output_1.txt"),
        ),
        (
            os.path.join(RESOURCE_FOLDER_PATH, "test_input_2.txt"),
            os.path.join(RESOURCE_FOLDER_PATH, "expected_output_2.txt"),
        ),
    ],
)
def test_from_file(test_input_file, expected_output_file):
    """
    Тест проверяет корректность вывода скрипта.
    На вход подаются файлы из папки 'test/resources/task3':

    - test_input_1.txt
    - test_input_2.txt
    """
    result = subprocess.run(
        ["python", os.path.join(SOLUTION_FOLDER_PATH, "task3.py"), test_input_file],
        stdout=subprocess.PIPE,
    )
    student_output = result.stdout.decode().strip()

    with open(expected_output_file, "r") as expected_output_file:
        expected_output_content = expected_output_file.read().strip()

    assert student_output == expected_output_content


@pytest.mark.parametrize(
    "test_input_file_1, test_input_file_2, test_input_file_3, expected_output_file",
    [
        (
            os.path.join(RESOURCE_FOLDER_PATH, "test_input_1.txt"),
            os.path.join(RESOURCE_FOLDER_PATH, "test_input_2.txt"),
            os.path.join(RESOURCE_FOLDER_PATH, "test_input_3.txt"),
            os.path.join(RESOURCE_FOLDER_PATH, "expected_output_combined.txt"),
        ),
    ],
)
def test_dict_multiple_files(
    test_input_file_1,
    test_input_file_2,
    test_input_file_3,
    expected_output_file,
):
    """
    Тест проверяет корректность вывода скрипта.
    На вход подается сразу все файлы из папки 'test/resources/task3':
    - test_input_1.txt test_input_2.txt test_input_3.txt
    """
    command_args = [
        "python",
        os.path.join(SOLUTION_FOLDER_PATH, "task3.py"),
        test_input_file_1,
        test_input_file_2,
        test_input_file_3,
    ]

    result = subprocess.run(
        command_args,
        stdout=subprocess.PIPE,
    )
    student_output_lines = result.stdout.decode().strip()

    with open(expected_output_file, "r") as expected_output_file:
        expected_output_lines = expected_output_file.read().strip()

    assert student_output_lines == expected_output_lines
