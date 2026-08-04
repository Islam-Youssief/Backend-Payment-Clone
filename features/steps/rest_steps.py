"""
This module imports all the REST language implementation steps into the project
so you can use them to write the tests. You can implement additional steps in
this module, or better yet, create additional step files in this folder for 
your custom steps.
"""
import requests
from behave_restful.lang import *

@when('the client sends 6 POST requests')
def step_impl(context):
    for _ in range(6):
        context.response = requests.post(
            context.request_url,
            headers=context.request_headers,
            json=context.request_json_payload
        )