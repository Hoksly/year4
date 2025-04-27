import pytest
from unittest.mock import patch
from app import try_parse_int, validate_a_b, try_parse_b, try_input_b  # adjust import
from geometry import classify_lines

# ----------------- try_parse_int -----------------

@pytest.mark.parametrize("input_value, expected", [
    ("42", 42),
    ("-127", -127),
    ("127", 127),
    ("128", None),
    ("-128", None),
    ("abc", None),
])
def test_try_parse_int(input_value, expected, capsys):
    result = try_parse_int(input_value)
    captured = capsys.readouterr()

    assert result == expected
    if expected is None:
        assert "спробуйте ще раз" in captured.out

# ----------------- validate_a_b -----------------

@pytest.mark.parametrize("a, b, expected", [
    (1, 0, True),
    (0, 1, True),
    (3, 4, True),
    (0, 0, False),
])
def test_validate_a_b(a, b, expected, capsys):
    result = validate_a_b(a, b)
    captured = capsys.readouterr()

    assert result == expected
    if not expected:
        assert "спробуйте ще раз" in captured.out

# ----------------- try_parse_b -----------------
@pytest.mark.parametrize("input_value, expected", [
    ("42.5", None),
    ("-127.0", None),
    ("127.999", None),
    ("0.0", None),
    ("1.23", None),
])
def test_try_parse_int_float_error(input_value, expected, capsys):
    result = try_parse_int(input_value)
    captured = capsys.readouterr()

    assert result == expected
    assert "не є ЦІЛИМ числом" in captured.out

def test_try_parse_b_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "25")
    result = try_input_b(1)
    assert result == 25

def test_try_parse_b_invalid_then_valid(monkeypatch):
    inputs = iter(["abc", "100"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = try_input_b(2)
    assert result == 100

# ----------------- try_input_b -----------------

def test_try_input_b_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "45")
    assert try_input_b(1) == 45

def test_try_input_b_invalid_then_valid(monkeypatch):
    inputs = iter(["-200", "50"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert try_input_b(2) == 50

def make_lines(a, b, c, k1, b1, k2, b2):
    line1 = {'A': a, 'B': b, 'C': c}
    line2 = {'A': -k1, 'B': 1, 'C': -b1}
    line3 = {'A': -k2, 'B': 1, 'C': -b2}
    return line1, line2, line3

# ----------------- classify_lines -----------------

@pytest.mark.parametrize("inputs, expected_class", [
    # Class 1 (coincide)
    ((-127, -1, 0, -127, 0, -127, 0), 1),
    ((127, -1, 0, 127, 0, 127, 0), 1),
    ((1, -1, 0, 1, 0, 1, 0), 1),
    ((127, -127, 0, 1, 0, 1, 0), 1),
    ((-127, -127, 0, -1, 0, -1, 0), 1),

    # Class 2 (parallel)
    ((127, -1, 127, 127, 126, 127, 125), 2),
    ((-127, -1, -127, -127, -126, -127, -125), 2),
    ((1, -1, 0, 1, 2, 1, 3), 2),
    ((-127, -127, -127, -1, 2, -1, -127), 2),
    ((-127, -1, -127, -127, -126, -127, 2), 2),

    # Class 3 (intersect at one point)
    ((127, -127, 127, 126, 0, 126, 0), 3),
    ((-127, -127, -127, -126, 0, -126, 0), 3),
    ((1, 1, 0, 8, 0, 4, 0), 3),
    ((-127, -127, -127, -2, -2, 127, 127), 3),
    ((-127, -127, -127, -126, -126, -1, -1), 3),
    ((127, 127, 127, 126, 126, 1, 1), 3),

    # Class 4 (intersect at two points)
    ((127, 127, 127, 126, 126, 126, 125), 4),
    ((-127, -127, -127, -126, -126, -126, -125), 4),
    ((1, 1, 0, 2, 1, 2, 2), 4),
    ((-127, -127, -127, -1, 2, 127, 127), 4),
    ((-127, -127, -127, -126, -124, -1, 2), 4),
    ((127, 127, 127, 126, 124, -1, 2), 4),

    # Class 5 (intersect at three points)
    ((127, 127, 0, 126, 126, 125, 126), 5),
    ((-127, -127, 0, -126, -126, -125, -126), 5),
    ((1, 1, 0, 1, 0, 2, -2), 5),
    ((-127, -127, -127, 1, 0, 126, 126), 5),
    ((-127, -127, -127, -127, -126, 1, 0), 5),
    ((127, 127, 127, 126, 125, 1, 0), 5),
])


def test_classify_lines(inputs, expected_class):
    a, b, c, k1, b1, k2, b2 = inputs
    line1, line2, line3 = make_lines(a, b, c, k1, b1, k2, b2)

    classification, points = classify_lines(line1, line2, line3)
    
    assert classification == expected_class


