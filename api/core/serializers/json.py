"""
This module provides classes and functions to make it easier to work with JSON.
"""
import collections.abc as cabc
import re


class Serializable:
    """
    Default implementation of the Serializable interface. Sub-classes can can implement :meth:`_add_data()` to support
    the full interface.

    ..  code-block:: python

        import api.core.serializers.json as sj

        class Person(sj.Serializable):
            def __init__(self, first_name, last_name):
                self.first_name = first_name
                self.last_name = last_name

            def _add_data(self, serialized):
                serialized.update(first_name=self.first_name, last_name=self.last_name)

        person = Person('John', 'Smith')
        person.to_dict()    # -> {'first_name': 'John','last_name': 'Smith'}
        person.to_json()    # -> {'firstName': 'John','lastName': 'Smith'}
    """

    def to_dict(self):
        """
        Serializes object using python case keys.

        :return:
            Dictionary representation of the object with python case keys.
        :rtype: dict
        """
        serialized = {}
        self._add_data(serialized)
        return serialized

    def to_json(self):
        """
        Serializes object using camel case keys.

        :return:
            Dictionary representation of the object with camel case keys.
        :rtype: dict
        """
        return keys_to_camel_case(self.to_dict())

    def _add_data(self, serialized):
        pass
        # raise NotImplementedError(f'Method _add_data() must be implemented in derived classes.')


def to_camel_case(py_attribute):
    """
    Converts a python attribute name (snake case) to camel case.

    :param str py_attribute:
        String in snake case format to be converted.

    :return:
        The converted camel case string.
    :rtype: str

    The following code example shows how this function works:

    ..  code-block:: python
        import api.core.serializers.json as sj

        sj.to_camel_case('simple')            # -> 'simple'
        sj.to_camel_case('snake_case')        # -> 'snakeCase'
        sj.to_camel_case('alreadyCamelCase')  # -> 'alreadyCamelCase'
    """
    underscore_clean = py_attribute.strip('_')
    words = underscore_clean.split('_')
    capitalized = words[0:1]
    capitalized.extend([word.capitalize() for word in words[1:]])
    return ''.join(capitalized)


def keys_to_camel_case(dictionary):
    """
    Converts all the keys in a dictionary to camel case going deep into values
    that are also dictionaries.

    :param dict dictionary:
        Dictionary object for which to convert all the keys to camel case.

    :return:
        The dictionary with all keys converted to camel case.
    :rtype: dict

    ..  code-block:: python
        import api.core.serializers.json as sj
        sample = {'first_case': {'first_example': 'first'}, 'secondCase': 2, 'ThirdCase': 3}
        sj.keys_to_camel_case(sample)  # -> {'firstCase': {'firstExample': 'first'}, 'secondCase': 2, 'ThirdCase': 3}
    """
    return _KeysConverter().to_camel_case(dictionary)


_FIRST_CAPITAL_RE = re.compile('(.)([A-Z][a-z]+)')
_ALL_CAPITAL_RE = re.compile('([a-z0-9])([A-Z])')


def to_python_case(camel_case):
    """
    Converts a camel case name to python attribute name (snake case).

    :param str camel_case:
        String in camel case format to be converted.

    :return:
        The converted snake case string.
    :rtype: str

    The following code example shows how this function works:

    ..  code-block:: python

        import api.core.serializers.json as sj

        sj.to_python_case('simple')            # -> 'simple'
        sj.to_python_case('camelCase')         # -> 'camel_case'
        sj.to_python_case('already_python')    # -> 'already_python'
    """
    first_cap_resolved = _FIRST_CAPITAL_RE.sub(r'\1_\2', camel_case)
    return _ALL_CAPITAL_RE.sub(r'\1_\2', first_cap_resolved).lower()


def keys_to_python_case(dictionary):
    """
    Converts all the keys in a dictionary to Python case going deep into values
    that are also dictionaries.

    :param dict dictionary:
        Dictionary object for which to convert all the keys to Python case.

    :return:
        The dictionary with all the keys converted to python case.
    :rtype: dict

    The following example shows how it works:

    ..  code-block:: python
        import api.core.serializers.json as sj
        sample = {'firstCase': {'firstExample': 'first'}, 'secondCase': 2, 'ThirdCase': 3}
        sj.keys_to_python_case(sample)  # -> {'first_case': {'first_example': 'first'}, 'second_case': 2, 'third_case': 3}
    """
    return _KeysConverter().to_python_case(dictionary)


def start_case_to_snake_case(text):
    """
    Converts a string from Start Case (space-separated) to snake_case.

    This function:
    - Strips leading and trailing whitespace.
    - Replaces one or more spaces with underscores.
    - Converts the entire string to lowercase.

    Example:
        start_case_to_snake_case("Expected Monthly Salary")
        -> "expected_monthly_salary"

    :param text: The input string in Start Case.
    :type text: str
    :return: The transformed string in snake_case.
    :rtype: str
    """
    text = text.strip()
    text = re.sub(r'\s+', '_', text)
    return text.lower()


class _KeysConverter:

    def to_camel_case(self, dictionary):
        return self._convert_property_names(dictionary, to_camel_case)

    def to_python_case(self, dictionary):
        return self._convert_property_names(dictionary, to_python_case)

    def _convert_property_names(self, original, convert_func):
        return {convert_func(k): self._normalize(v, convert_func) for k, v in original.items()}

    def _normalize(self, value, convert_func):
        if isinstance(value, list):
            return [self._normalize(o, convert_func) for o in value]
        if isinstance(value, dict):
            return self._convert_property_names(value, convert_func)
        return value


class JsonObject(Serializable):
    """
    This class wraps a dictionary object and allows accessing values using the
    keys in the dictionary as attributes of the object.

    This class handles attributes that contain other dictionaries (JSON object)
    and lists (JSON arrays) returning an appropriate wrapper. This makes it
    easier to handle nested objects and arrays inside the main dictionary.

    If the attribute specified is not in the dictionary, it returns ``None``,
    which makes this class suitable for PATCH payloads.

    ..  code-block:: python

        json_obj = {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien,
            'stars': 5,
            'categories': ['fiction', 'fantasy', 'adventure'],
            'editions': [
                {
                    'edition': 1,
                    'year': 1952
                },
                {
                    'edition': 2,
                    'year': 1956
                }
            ],
            'reference': {
                'isbn': '12345678',
                'year': '2020'
            }

        }

        obj = JsonObject(json_obj)
        obj.title               # -> 'The Lord of the Rings'
        obj.title               # -> 'J.R.R. Tolkien'
        obj.copyright           # -> None
        obj.stars               # -> 5
        obj.categories[1]       # -> 'fantasy'
        obj.editions[0].year    # -> 1952
    """

    def __init__(self, json_obj):
        self._obj = keys_to_python_case(json_obj)

    def __getattr__(self, name):
        return self._get_from_dict(name)

    def __bool__(self):
        return True if self._obj else False

    def _get_from_dict(self, name):
        value = self._obj.get(name)
        return _wrap_value(value)

    def _add_data(self, serialized):
        serialized.update(self._obj)


class JsonArray(cabc.Sequence):
    """
    This class wraps a JSON array into a similar interface to a list.

    It also wraps the contents of the array into :class:`JsonObject` or
    :class:`JsonArray` where applies.

    ..  code-block:: python

        json_array = [
            1,
            'two',
            {
                'prop': 'value'
            }
        ]

        arr = JsonArray(json_array)
        arr[0]          # -> 1
        arr[-3]         # -> 1
        arr[1]          # -> 'two'
        arr[-2]         # -> 'two'
        arr[2].prop     # -> 'value'            # Notice
        arr[-1].prop    # -> 'value'            # Notice
        arr[3]          # -> raises IndexError
        arr[-4]         # -> raises IndexError
    """

    def __init__(self, json_array):
        self._array = json_array

    def __contains__(self, item):
        return item in self._array

    def __getitem__(self, index):
        return _wrap_value(self._array[index])

    def __iter__(self):
        return iter([_wrap_value(v) for v in self._array])

    def __len__(self):
        return len(self._array)


def _wrap_value(value):
    if isinstance(value, dict):
        return JsonObject(value)
    if isinstance(value, list):
        return JsonArray(value)
    return value