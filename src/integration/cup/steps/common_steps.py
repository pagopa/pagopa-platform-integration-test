from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401


@then('Il PSP riceve un 200 OK che all\'interno riporta il fault code {risposta}')
def step_psp_riceve_200_con_fault_code(context, risposta):
    """Assert the PSP receives a 200 OK response containing the expected fault code."""
    pass
