import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from json_dict_diff import diff, ValidationException


def test_validation_exception():
    class A:
        pass

    with pytest.raises(ValidationException):
        diff(A(), 1)
    with pytest.raises(ValidationException):
        diff(1, A())
    with pytest.raises(ValidationException):
        diff(1, {"a": A()})
    with pytest.raises(ValidationException):
        diff(1, [A()])
    with pytest.raises(ValidationException):
        diff(1, (A()))
    with pytest.raises(ValidationException):
        diff({"a": A()}, 1)
    with pytest.raises(ValidationException):
        diff([A()], 1)
    with pytest.raises(ValidationException):
        diff((A()), 1)


def test_simple_equal():
    assert diff("a", "a") is None
    assert diff(1, 1) is None
    assert diff(1.0, 1.0) is None
    assert diff(True, True) is None
    assert diff(False, False) is None
    assert diff({}, {}) is None
    assert diff([], []) is None
    assert diff((), ()) is None
    assert diff(set(), set()) is None
    assert diff(None, None) is None


def test_simple_unequal():
    assert diff("a", "b") == ("a", "b")
    assert diff(1, 2) == (1, 2)
    assert diff(1.0, 2.0) == (1.0, 2.0)
    assert diff(True, False) == (True, False)
    assert diff(False, True) == (False, True)
    assert diff({}, []) == ({}, [])
    assert diff([], {}) == ([], {})
    assert diff((), {}) == ((), {})
    assert diff(set(), {}) == (set(), {})
    assert diff(None, 1) == (None, 1)


def test_equal():
    assert diff({"a": 1}, {"a": 1}) is None
    assert diff({"a": 1, "b": {"c": True}}, {"a": 1, "b": {"c": True}}) is None
    # order in lists should not matter
    assert diff({"a": 1, "b": {"c": [3, 2, 4, 1]}}, {"a": 1, "b": {"c": [1, 4, 3, 2]}}) is None
    # multiple identical elements in lists should not matter
    assert (
        diff(
            {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
            {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
        )
        is None
    )
    assert (
        diff(
            {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [2, 1]}]}},
            {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
        )
        is None
    )
    assert (
        diff(
            {"a": 1, "b": {"c": [[{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [2, 1]}]]}},
            {"a": 1, "b": {"c": [[{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]]}},
        )
        is None
    )
    # also for tuples
    assert (
        diff(
            {"a": 1, "b": {"c": ({"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [2, 1]})}},
            {"a": 1, "b": {"c": ({"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]})}},
        )
        is None
    )
    # and sets
    assert diff(set((1, 2)), set((1, 2))) is None
    # should also work if wrapped in a list
    assert (
        diff(
            [{"a": 1, "b": {"c": ({"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [2, 1]})}}],
            [{"a": 1, "b": {"c": ({"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]})}}],
        )
        is None
    )


def test_unequal():
    assert diff({"a": 1}, {"a": 2}) == {"a": (1, 2)}
    assert diff({"a": 1, "b": {"c": True}}, {"a": 1, "b": {"c": False}}) == {"b": {"c": (True, False)}}
    assert diff({"a": 1, "b": {"c": True}}, {"a": 2, "b": {"c": False}}) == {"a": (1, 2), "b": {"c": (True, False)}}
    # order in lists should not matter (inserting/deleting/updating elements)
    assert diff({"a": 1, "b": {"c": [3, 2, 4, 1]}}, {"a": 1, "b": {"c": [1, 4, 3, 2, 8]}}) == {"b": {"c": [(None, 8)]}}
    assert diff({"a": 1, "b": {"c": [3, 2, 4, 1]}}, {"a": 1, "b": {"c": [4, 3, 2]}}) == {"b": {"c": [(1, None)]}}
    assert diff({"a": 1, "b": {"c": [3, 2, 4, 1]}}, {"a": 1, "b": {"c": [4, 8, 3, 2]}}) == {"b": {"c": [(1, 8)]}}
    # if values of the same types are substituted, the substition should still be deterministic
    assert diff({"a": 1, "b": {"c": [True, 2, 4, 1]}}, {"a": 1, "b": {"c": [4, 8, False, 2]}}) == {
        "b": {"c": [(True, False), (1, 8)]}
    }
    assert diff({"a": 1, "b": {"c": [3, False, 4, 1, True]}}, {"a": 1, "b": {"c": [4, True, 8, 3, True]}}) == {
        "b": {"c": [(False, True), (1, 8)]}
    }
    # multiple identical elements in lists should not matter
    assert diff(
        {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
        {"a": 1, "b": {"c": [{"d": 1, "x": [1]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
    ) == {"b": {"c": [{"x": [(2, None)]}]}}
    assert diff(
        {"a": 1, "b": {"c": [{"d": 1, "x": [1]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
        {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
    ) == {"b": {"c": [{"x": [(None, 2)]}]}}
    assert diff(
        {"a": 1, "b": {"c": [{"d": 2, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [2, 1]}]}},
        {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
    ) == {"b": {"c": [{"d": (2, 1)}]}}
    assert diff(
        {"a": 1, "b": {"c": [{"d": 2, "x": [1]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
        {"a": 1, "b": {"c": [{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]}},
    ) == {"b": {"c": [{"d": (2, 1), "x": [(None, 2)]}]}}
    assert diff(
        {"a": 1, "b": {"c": [[{"d": 2, "x": [1]}, {"e": False, "x": 1}, {"d": 1, "x": [2, 1]}]]}},
        {"a": 1, "b": {"c": [[{"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]}]]}},
    ) == {"b": {"c": [[{"d": (2, 1), "x": [(None, 2)]}, {"e": (False, 1), "x": (1, True)}]]}}
    # also for tuples
    assert diff(
        {"a": 1, "b": {"c": ({"d": 1, "x": [1, 2]}, {"e": [1, 2], "x": True}, {"d": 1, "x": [2, 1]})}},
        {"a": 1, "b": {"c": ({"d": 1, "x": [1, 2]}, {"e": 1, "x": True}, {"d": 1, "x": [1, 2]})}},
    ) == {"b": {"c": [{"e": ([1, 2], 1)}]}}
    # and sets (be aware that set considers e.g. 1 and True to be equal)
    assert diff(set((2, 3)), set((2, True))) == [(3, True)]
