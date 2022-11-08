import hypothesis.strategies as st


def return_nested_dictionary() -> st.SearchStrategy:
    """Returns a simple nested dictionary containing
    one level of nesting

    Example output format:
    {
        "strings": <str>,
        "dict": {
            "nested_strings": <str>,
            "nested_ints": <int>
        }
    }

    :return: Hypothesis search strategy
    """
    return st.fixed_dictionaries({
        "strings": st.characters(),
        "dict": st.fixed_dictionaries({
            "nested_strings": st.characters(),
            "nested_ints": st.integers()
        })
    })


def return_nested_dictionary_list_of_dicts(nested_list_len: int) -> st.SearchStrategy:
    """Returns a nested dictionary with a list of dictionaries
    nested within the main dictionary

    :param nested_list_len: controls max length of nested list

    Example output format:
    {
        "my_datetime": <datetime>,
        "my_list": [
            {
                "my_uuid": <uuid.UUID>,
                "my_string": <str>
            },
            {
                "my_uuid": <uuid.UUID>,
                "my_string": <str>
            },
            {
                "my_uuid": <uuid.UUID>,
                "my_string": <str>
            },
        ]
    }

    :return: Hypothesis search strategy
    """
    return st.fixed_dictionaries({
            "my_datetime": st.datetimes(),
            "my_list": st.lists(
                st.fixed_dictionaries({
                    "my_uuid": st.uuids(),
                    "my_string": st.characters()
                }),
                max_size=nested_list_len)
        })