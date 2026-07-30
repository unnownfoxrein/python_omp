import pytest

from solution.task2 import not_bad, verbing


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("walk", "walking"),
        ("construct", "constructing"),
        ("jump", "jumping"),
        ("coding", "codly"),
        ("a", "a"),
        ("it", "it"),
        ("go", "go"),
        ("", ""),
        ("constructing", "constructly"),
        ("lying", "lyly"),
        ("being", "bely"),
        ("be", "be"),
    ],
)
def test_verbing(input_str, expected_output) -> None:
    assert verbing(input_str) == expected_output


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("This is not a bad example.", "This is good example."),
        ("This is not that bad.", "This is good."),
        ("This is bad, not good.", "This is bad, not good."),
        ("Nothing here to replace.", "Nothing here to replace."),
        ("Not here, not bad.", "Not here, good."),
        ("Bad after not.", "Bad after not."),
        ("This is really not not bad.", "This is really good."),
        ("Not Bad != not bad.", "Not Bad != good."),
        ("Not enough information to decide.", "Not enough information to decide."),
        ("Bad comes before not.", "Bad comes before not."),
    ],
)
def test_not_bad(input_str, expected_output) -> None:
    assert not_bad(input_str) == expected_output
