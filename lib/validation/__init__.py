from lib.exceptions import *
import re


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


def check_boolean(event, keys, body=True):
    """
    Because Dynamo can't have a boolean as a RangeKey, I have
    implemented booleans there as "yes" or "no". This tests for that.
    :param event: The event object from Lambda.
    :param keys: List of keys to test.
    :param body: Check in the body or in the event itself.
    :return: Nothing if success, exception if failed.
    """
    for key in keys:
        if body is True:
            if key not in event['body'].keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if not re.match(r"^(yes|no)$", event['body'][key]):
                raise BadRequestException("Key '%s' contains an invalid boolean value ('%s')." % (key, event['body'][key]))
        else:
            if key not in event.keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if re.match(r"yes|no", event[key]):
                raise BadRequestException("Key '%s' contains an invalid boolean value ('%s')." % (key, event[key]))


def check_relation(foreign_table, key, value):
    """
    Check a foreign table for an entry. It's basically relations, with no-SQL!
    :param foreign_table: The foreign table object.
    :param key: The key to search for in the foreign table.
    :param value: The value to search for in the foreign table.
    :return: None if good, Exception if bad.
    """
    # Get response
    try:
        response = foreign_table.get_item(Key={key: value})
    except ClientError as ce:
        raise InternalServerException(ce.message)

    if 'Item' not in response:
        raise NotFoundException("Object '%s' for relation not found in table '%s'." % (value, foreign_table.table_name))
