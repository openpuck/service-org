from lib.exceptions import *

def string_length(input_string, num_chars):
    """
    Validate a territory code.
    """
    if len(input_string) > num_chars:
        raise BadRequestException("Value '%s' has too many characters (max: %d)." % (input_string, num_chars))

def check_keys(keys, event, body=True):
    """
    Test for the existance of the given list of keys in the event.
    """
    for key in keys:
        if body is True:
            if key not in event['body'].keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if len(event['body'][key]) is 0:
                raise BadRequestException("Key '%s' is empty." % key)
        else:
            if key not in event.keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if len(event[key]) is 0:
                raise BadRequestException("Key '%s' is empty." % key)
