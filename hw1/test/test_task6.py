import os
import re
import subprocess

import pytest

SOLUTION_FOLDER_PATH = "solution"
RESOURCE_FOLDER_PATH = os.path.join("test", "resources", "task6")


def parse_nl_helper(output):
    pattern = r"\s*(\d+)\s*(.*)"
    match = re.match(pattern, output)
    if not match:
        return

    number = int(match.group(1))
    remaining_string = match.group(2)
    return number, remaining_string


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
def test_compare_lines(test_input_file: str, expected_output_file: str) -> None:
    result = subprocess.run(
        ["python", os.path.join(SOLUTION_FOLDER_PATH, "task6.py"), test_input_file],
        stdout=subprocess.PIPE,
    )
    student_output_lines = result.stdout.decode().strip().splitlines()

    with open(expected_output_file, "r") as expected_output_file:
        expected_output_lines = expected_output_file.read().strip().splitlines()

    for expected_line, output_line in zip(expected_output_lines, student_output_lines):
        assert parse_nl_helper(expected_line) == parse_nl_helper(output_line)
