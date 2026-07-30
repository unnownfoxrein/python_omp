import os
import re
import subprocess

import pytest

SOLUTION_FOLDER_PATH = "solution"
RESOURCE_FOLDER_PATH = os.path.join("test", "resources", "task5")


def parse_wc_helper(output):
    pattern = r"(\d+)\s+(\d+)\s+(\d+)\s+(.*)"
    match = re.search(pattern, output)

    if not match:
        return None
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        match.group(4),
    )


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
        (
            os.path.join(RESOURCE_FOLDER_PATH, "test_input_3.txt"),
            os.path.join(RESOURCE_FOLDER_PATH, "expected_output_3.txt"),
        ),
    ],
)
def test_compare_stats(test_input_file, expected_output_file):
    """
    Тест проверяет корректность вывода скрипта.
    На вход подаются файлы из папки 'test/resources/task5':

    - test_input_1.txt
    - test_input_2.txt
    - test_input_3.txt
    """
    result = subprocess.run(
        ["python", os.path.join(SOLUTION_FOLDER_PATH, "task5.py"), test_input_file],
        stdout=subprocess.PIPE,
    )
    student_output = result.stdout.decode().strip()
    with open(expected_output_file, "r") as expected_output_file:
        expected_output_content = expected_output_file.read().strip()
    assert parse_wc_helper(student_output) == parse_wc_helper(expected_output_content)


@pytest.mark.parametrize(
    "test_input_file_1, test_input_file_2, test_input_file_3, expected_output_file",
    [
        (
            f"{RESOURCE_FOLDER_PATH}/test_input_1.txt",
            f"{RESOURCE_FOLDER_PATH}/test_input_2.txt",
            f"{RESOURCE_FOLDER_PATH}/test_input_3.txt",
            f"{RESOURCE_FOLDER_PATH}/expected_output_combined.txt",
        ),
    ],
)
def test_compare_stats_total(
    test_input_file_1,
    test_input_file_2,
    test_input_file_3,
    expected_output_file,
):
    """
    Тест проверяет корректность вывода скрипта.
    На вход подается сразу все файлы из папки 'test/resources/task5':
    - test_input_1.txt test_input_2.txt test_input_3.txt
    """
    command_args = [
        "python",
        os.path.join(SOLUTION_FOLDER_PATH, "task5.py"),
        test_input_file_1,
        test_input_file_2,
        test_input_file_3,
    ]

    result = subprocess.run(
        command_args,
        stdout=subprocess.PIPE,
    )
    student_output_lines = result.stdout.decode().strip().splitlines()

    with open(expected_output_file, "r") as expected_output_file:
        expected_output_lines = expected_output_file.read().strip().splitlines()

    for expected_line, output_line in zip(expected_output_lines, student_output_lines):
        assert parse_wc_helper(expected_line) == parse_wc_helper(output_line)
