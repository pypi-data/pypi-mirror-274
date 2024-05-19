

import json
import os
from handlebars import Handlebars


def _run_test(template, data, expected, helpers={}):
    for helper_key, helper_func in helpers.items():
        Handlebars.registerHelper(helper_key, helper_func)
    template = Handlebars.compile(template)
    actual = template(data)
    assert actual == expected

def _test_helper():
    return "test"

def test_helper():
    _run_test(
        "Name: {{name}}, {{testf}}",
        { "name": "Jane" },
        "Name: Jane, test",
        {"testf": _test_helper}
    )
