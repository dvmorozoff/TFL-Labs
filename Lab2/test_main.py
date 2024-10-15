import pytest

from main import membership, equivalence

test_data = [
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    ("aba", True),
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    (0, False),
    (0, False),
    ("aabba", True),
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    (0, False),
    (1, True),
    (0, False),
    (0, False),
    (0, False),
    (0, False),
    ("TRUE", True)
]

@pytest.mark.parametrize("input_value, expected_output", test_data)
def test_functions(input_value, expected_output):
    if isinstance(input_value, int):
        result = membership(input_value)
        assert result == expected_output
        print(f"Input: {input_value}, Output: {result}, Expected: {expected_output}")
    elif isinstance(input_value, str):
        result = equivalence(input_value)
        assert result == expected_output
        print(f"Input: {input_value}, Output: {result}, Expected: {expected_output}")

if __name__ == "__main__":
    pytest.main()
