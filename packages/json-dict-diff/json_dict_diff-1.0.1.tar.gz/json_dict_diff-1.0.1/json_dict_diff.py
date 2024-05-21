from typing import List, Dict, Union, Tuple, Set

JDict = Union[int, float, str, List["Result"], Dict[str, "Result"], Tuple["Result"], Set["Result"], None]


class ValidationException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def _similarity_score(a: JDict, b: JDict) -> float:
    """
    Helper function to find a similarity score of two JDicts.
    This is done by comparing the elements or subelements of lists/dicts/sets/tuples and counting
    the matches.
    """
    if type(a) is not type(b):
        return 0

    if a is None and b is None:
        return 1

    if a is None or b is None:
        return 0

    # If they have the same type at least return 0.5
    if isinstance(a, (int, str, float, bool)):
        if a == b:
            return 1
        else:
            return 0.5

    elif isinstance(a, (tuple, list, set)):
        a = list(a)
        b = list(b)

        if not a or not b:
            return 0.5

        # Find best match witch score matrix,
        # remove best match and find best score again of the reduced lists
        score_matrix = []

        for i1, v1 in enumerate(a):
            for i2, v2 in enumerate(b):
                score_matrix.append(((i1, i2), _similarity_score(v1, v2)))

        score_matrix.sort(key=lambda x: x[1], reverse=True)

        # We can assume that at least one element is present
        res = score_matrix[0][1]

        a_updated = a.copy()
        b_updated = b.copy()

        del a_updated[score_matrix[0][0][0]]
        del b_updated[score_matrix[0][0][1]]

        res += _similarity_score(a_updated, b_updated)

        return res

    elif isinstance(a, dict):

        if not a or not b:
            return 1

        res = 1

        for k1, v1 in a.items():
            if k1 in b.keys():
                res += _similarity_score(v1, b[k1])

        return res

    else:
        raise ValidationException(f"Invalid type  => [{type(a)}]")


def _diff(a: JDict, b: JDict) -> JDict:
    """
    Actual diff function only to be called by `diff`.
    """
    if type(a) is not type(b):
        return (a, b)

    if a is None and b is None:
        return None

    if a is None:
        return (None, b)

    if b is None:
        return (a, None)

    if isinstance(a, (int, str, float, bool)):
        if a == b:
            return None
        else:
            return (a, b)

    elif isinstance(a, (tuple, list, set)):
        a = list(a)
        b = list(b)

        res = []

        # Find most suitable match for each element in a
        b_updated = b.copy()
        for v1 in a:
            b_found = 0 if len(b_updated) > 0 else None
            score = 0
            for i, v2 in enumerate(b_updated):
                if (s := _similarity_score(v1, v2)) > score:
                    b_found = i
                    score = s

            # If we did not find a match assume that the element was deleted
            # If we did, append their diff
            if b_found is None:
                res.append((v1, None))
            else:
                if (d := diff(v1, b_updated[b_found])) is not None:
                    res.append(d)
                del b_updated[b_found]

        # Add remaining elements in bas newly created
        for v2 in b_updated:
            if v2 is not None:
                res.append((None, v2))

        if not res:
            return None

        return res

    elif isinstance(a, dict):
        res = {}

        b_updated = b.copy()
        for k1, v1 in a.items():
            if k1 in b_updated.keys():
                if (d := diff(v1, b_updated[k1])) is not None:
                    res[k1] = d
                del b_updated[k1]

        # Add remaninig elements in b as newly created
        for k2, v2 in b_updated.items():
            res[k2] = (None, v2)

        if not res:
            return None

        return res

    else:
        raise ValidationException(f"Invalid type => [{t}]")


def validate(a: JDict):
    """
    This function can be used to validate the type of a JDict object at runtime,
    If the JDict contains a invalid type, a `ValidationException` is raised.
    """
    if a is None:
        return

    if isinstance(a, (int, str, float, bool)):
        return
    elif isinstance(a, (tuple, list, set)):
        for v in a:
            validate(v)
    elif isinstance(a, dict):
        for k, v in a.items():
            if not isinstance(k, str):
                raise ValidationException(f"Invalid type => [{type(a)}]")
            validate(v)
    else:
        raise ValidationException(f"Invalid type => [{type(a)}]")


def diff(a: JDict, b: JDict) -> JDict:
    """
    This function can be used to diff two dictionaries.
    The diff is represented as a dictionary where insertions/deletions/substititons are represented as tuples.
    E.g the following two dictionaries:

    ```py
    diff(
      { "a": [ { "b": 1, "c": True }, 1.0, "x" ], "d": 1 },
      { "a": [ { "b": 2, "c": True }, 1.0, "y", True ] }
    )
    ```

    will result in the following diff:

    ```py
    { "a": [ { "b": (1, 2) }, ("x", "y"), (None, True) ], "d": (1, None) }
    ```

    Here the tuples `(1, 2), ("x", "y"), (None, True), (1, None)` represent the substitions that happened.
    `None` implies that a object was either removed or added.

    If there is no diff (e.g.: `diff({ "a": 1 }, { "a": 1 })`) the result will be `None`. In this sense,
    this function can also be used to compare two json-compatible dictionaries.
    """

    validate(a)
    validate(b)
    return _diff(a, b)
