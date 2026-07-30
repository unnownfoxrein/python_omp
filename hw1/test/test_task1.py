import pytest

from solution.task1 import is_correct, linear_merge, remove_adjacent


@pytest.mark.parametrize(
    "input_list, output_list",
    [
        ([], []),
        ([7], [7]),
        ([4, 4, 4, 4], [4]),
        ([1, 1, 2, 2, 3, 3], [1, 2, 3]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([5, 5, 2, 2, 2, 5, 5], [5, 2, 5]),
        ([10, 20, 20, 10, 10, 10, 30, 30], [10, 20, 10, 30]),
        ([1, 1, 1, 2, 2, 3, 3, 3, 3], [1, 2, 3]),
    ],
)
def test_remove_adjacent(input_list, output_list) -> None:
    assert remove_adjacent(input_list) == output_list


@pytest.mark.parametrize(
    "xs, ys, output_list",
    [
        ([], [], []),
        ([], [2, 4, 6], [2, 4, 6]),
        ([1, 3, 5], [], [1, 3, 5]),
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3], [1, 2, 3], [1, 1, 2, 2, 3, 3]),
        ([4, 4, 4], [4, 4, 4], [4, 4, 4, 4, 4, 4]),
        ([10, 20, 30], [5, 15, 25], [5, 10, 15, 20, 25, 30]),
        ([-5, -3, 0], [-10, -8, -2], [-10, -8, -5, -3, -2, 0]),
    ],
)
def test_linear_merge(xs, ys, output_list):
    assert linear_merge(xs, ys) == output_list


@pytest.mark.parametrize(
    "brackets, result",
    [
        ("()", True),
        ("[]", True),
        ("{}", True),
        ("[()]", True),
        ("[{}]", True),
        ("{[]}", True),
        ("[({})]", True),
        ("", True),  # An empty sequence is valid
        ("(", False),
        (")", False),
        ("[", False),
        ("]", False),
        ("{", False),
        ("}", False),
        ("[)", False),
        ("[({}]", False),
        ("{[}]", False),
        ("[", False),
        ("]", False),
        ("[}", False),
        ("[)", False),
        ("[({}]", False),
        ("{[}]", False),
        ("[()", False),
        ("[])", False),
        ("({}}", False),
        ("[{]}", False),
        ("{[)", False),
        ("{[]((((", False),
        ("[{[}]", False),
        ("[({)}]", False),
    ],
)
def test_is_correct(brackets, result):
    assert is_correct(list(brackets)) == result
