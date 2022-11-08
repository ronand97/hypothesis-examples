# Intro

Python has a package for attribute testing called Hypothesis.  This is just a brief document containing some of my thoughts and any “gotchas”.

# Useful resources


https://hypothesis.readthedocs.io/en/latest/

https://www.youtube.com/watch?v=mkgd9iOiICc


In the future I'd like to look at mutation testing:

https://mutatest.readthedocs.io/en/latest/




# How to start writing an attribute test with example

A few things I like to think of are:

* length

* object types

* expected changes present

* handles edge cases

For example:

Given a standalone function

```python
def time_between_dates(dates=List[np.datetime64]) -> List[datetime.timedelta]:
    """
    Take in list of datetime objects. Return list of pairwise timedeltas
    between them as sorted. e.g. timedelta between [0] and [1], then
    between [1] and [2]

    :param dates: list of datetimes
    :return: list of (len(dates) - 1) pairwise timedeltas
    """
    dates.sort()
    if len(dates) > 1:
        timedeltas = [dates[i-1] - dates[i] for i in range(1, len(dates))]
        return timedeltas
    else:
        return [pd.Timedelta(0)]
```


We can see that, for an input list of length n we expect the return list to be of length n-1 except where the list is of length 0 or 1.

A simple attribute test would be to check that the lengths are as expected and that the return types are of type timedelta - we separately handle specific edge cases in our pytest parameterized test cases.

Example implementation of attribute test for the above function:

```python
from typing import List
from hypothesis import given
from hypothesis.strategies import dates, lists
from datetime import timedelta

@given(lists(dates(), min_size=2))
def test_attributes(dates: List[datetime]):
    timedeltas = time_between_dates(dates)
    assert len(timedeltas) == (len(dates) - 1)
    assert all([isinstance(x, timedelta) for x in timedeltas])
```


Breaking down the above test:

1. Importing `given` lets us decorate any test function to feed in auto-generated data

2. Importing hypothesis `strategies` are what lets us define what datatype we want to feed in

3. We decorate our function with the given statement and the parameters are the data types. In this case we want lists of dates, so we have wrapped `dates()` in a `lists()` strategy, where we have set the minimum length of the list == 2 as we know that the edge cases are handled elsewhere

4. We have specifically referenced our list of dates in our test function as the first input parameter

# Example pandas dataframe generation
Can be found in `hypothesis-examples\hypothesis_examples\dataframes.py`

# Gotchas

* Pandas is sometimes funny about being fed in list entries as cell elements. Setting the parameter dtype="object" can usually fix this

* the column function from hypothesis should give you a pandas series with elements sampled from the given dtype parameter. However I found this tempermental and I had more success just defining elements directly from strategies. e.g. `column("my_col_name", elements=lists(dates()))`. If necessary, you can also add in dtype here `column("my_col_name", elements=lists(dates()), dtype="object")`

* Pandas and numpy sometimes have their own return types which won’t match up. e.g. if you want to check the return type is timedelta, sometimes it might be pandas.Timedelta. In this case, I changed my test to look for pd.Timedelta instead. Similarly I found a case with a numpy `bool` return type being `numpy.bool_` which failed my `assert isinstance(var_name, bool)` assertion. In this bool case, I changed the underlying function by wrapping the output in `bool()` to force the type as I wanted it.

* Tests that take too long can trigger unrelated error messages. For example, I kept getting a flaky test error (as seen here  ) when it was my test taking too long. To get around this for long-running functions/methods, you can do from hypothesis import settings and decorate your test function

```python
from hypothesis import given, settings

@settings(deadline=10000  # 10[s] in [ms])
@given(<whatever>)
def my_function():
```

* In the same way you’d import and decorate in the previous bullet point, you can change the verbosity of the tests to get detailed outputs. So from hypothesis import Verbosity and then in the settings decorator, you can write `@settings(verbosity=Verbosity.verbose)`. If using pycharm, pycharm auto quietens test results which you can turn off by searching for pytest and toggle the setting:

* Unique strings. Whilst it looks possible to generate unique strings I could not figure out how to do this in the context of a dataframe. Hence I generated UUIDs instead and wrapped them in strings.