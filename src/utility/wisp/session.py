from src.utility.wisp import constants


def skip_tests(context):
    return getattr(context, constants.SKIP_TESTS)


def set_skip_tests(context, value):
    setattr(context, constants.SKIP_TESTS, value)


def get_test_data(context):
    '''
    '''

    return get_flow_data(context, constants.SESSION_DATA_TEST_DATA)


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
