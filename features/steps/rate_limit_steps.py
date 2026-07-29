"""
Custom step definitions for rate limiting tests.
"""
from behave import when


@when('the request sends POST {count:d} times')
def step_send_post_n_times(context, count):
    """Send the same POST request N times and store the last response."""
    headers = context.request_headers if hasattr(context, 'request_headers') else None
    payload = context.request_json_payload if hasattr(context, 'request_json_payload') else None

    for i in range(count):
        context.response = context.session.post(
            context.request_url,
            json=payload,
            headers=headers
        )
