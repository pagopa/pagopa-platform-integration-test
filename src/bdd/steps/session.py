import logging
# import constants as constants
from src.utility import constants, utils

def clear_session(context):

    setattr(context, constants.SESSION_DATA, {})
    setattr(context, constants.SKIP_TESTS, False)

# ==============================================

def skip_tests(context):
    return getattr(context, constants.SKIP_TESTS)

# ==============================================

def set_skip_tests(context, value):
    setattr(context, constants.SKIP_TESTS, value)

# ==============================================

# def set_test_data(context, test_data):
#     '''
#     Set the data generated for trigger primitive (i.e. nodoInviaRPT, nodoInviaCarrelloRPT)
#     in the session data.
#     The test_data field is used to encapsulate starting RPTs' information in order to re-use
#     them in other kind of requests.
#     '''
#
#     session_data = getattr(context, constants.SESSION_DATA)
#     session_data[constants.SESSION_DATA_TEST_DATA] = test_data
#     set_flow_data(context, constants.SESSION_DATA_TEST_DATA, test_data)

# ==============================================

def get_test_data(context):
    '''
    '''

    return get_flow_data(context, constants.SESSION_DATA_TEST_DATA)

# ==============================================

def set_flow_data(context, field_name, value):
    nested_fields = field_name.split('.')
    session_data = getattr(context, constants.SESSION_DATA)
    analyzed_object = session_data
    for index, field in enumerate(nested_fields):
        if field not in analyzed_object:
            analyzed_object[field] = dict()
        if index == len(nested_fields) - 1:
            analyzed_object[field] = value
        else:
            analyzed_object = analyzed_object[field]

# ==============================================

def get_flow_data(context, field_name):
    try:
        nested_fields = field_name.split('.')
        session_data = getattr(context, constants.SESSION_DATA)
        analyzed_object = session_data
        for field in nested_fields:
            if field in analyzed_object:
                analyzed_object = analyzed_object[field]
            else:
                return None
        return analyzed_object
    except Exception as e:
        return None

# ==============================================

# def debug_session_data(context):
#     session_data = getattr(context, constants.SESSION_DATA)
#     logging.debug(f"""
#                ==========session data==========
#                {session_data}
#                ================================
#                """)