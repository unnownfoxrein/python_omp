import pytest

from solution.task4 import matrix_pretty_print, matrix_product


@pytest.mark.parametrize(
    "mat_a, mat_b, expected_result",
    [
        ([[3]], [[4]], [[12]]),
        (
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8], [9, 10], [11, 12]],
            [[58, 64], [139, 154]],
        ),
        (
            [[1, 2], [3, 4]],
            [[5, 6], [7, 8]],
            [[19, 22], [43, 50]],
        ),
        (
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8], [9, 10], [11, 12]],
            [[58, 64], [139, 154]],
        ),
    ],
)
def test_matrix_product(mat_a, mat_b, expected_result):
    assert matrix_product(mat_a, mat_b) == expected_result


def wrap_display_matrix(pretty_mat, step):
    return f"\n{step*'-'}\n{pretty_mat}\n{step*'-'}"


def test_display_pretty_print():
    # Чтобы удобнее на вывод смотреть в CI.

    print(wrap_display_matrix(matrix_pretty_print([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 1))
    print(wrap_display_matrix(matrix_pretty_print([[11, -4, 6, 123], [12, -900, 2, 5]]), 1))
