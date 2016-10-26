import re
from lib.exceptions import *
from decimal import Decimal, InvalidOperation
from boto3.dynamodb.conditions import Key

# Validation Modes
MODE_CREATE = "CREATE"
MODE_READ = "READ"
MODE_UPDATE = "UPDATE"
MODE_DELETE = "DELETE"

# Data Type Attributes
BOOLEAN_FIELDS = ['is_women', 'is_active']


def _build_key_expression_from_dict(data):
    """
    Build a KeyConditionExpression object from a dictionary of key:value pairs.
    :param data: The dictionary of data.
    :return: A KeyConditionExpression object
    """
    key_object = None
    for key in data.keys():
        if key_object is None:
            key_object = Key(key).eq(data[key])
        else:
            key_object = key_object & Key(key).eq(data[key])

    return key_object


def _string_length(input_string, num_chars):
    """
    Check that a given string is of the given length.
    :param input_string: The string to test.
    :param num_chars: The number of characters that should be in that string.
    :return: None if success, Exception if failed.
    """
    if len(input_string) > num_chars:
        raise BadRequestException("Value '%s' has too many characters "
                                  "(max: %d)." % (input_string, num_chars))


def _check_keys(keys, event, body=True):
    """
    Check that all of the given keys exist within an event. Two code paths
    for the ability to test the event and the event body.
    :param keys: List of keys to test for.
    :param event: The Lambda event object.
    :param body: Boolean of whether to check the body or not.
    :return: None if success, Exception if failed.
    """
    for key in keys:
        if body is True:
            if key not in event['body'].keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if not isinstance(event['body'][key], int):
                if len(event['body'][key]) is 0:
                    raise BadRequestException("Key '%s' is empty." % key)
        else:
            if key not in event.keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if len(event[key]) is 0:
                raise BadRequestException("Key '%s' is empty." % key)


def _check_boolean(event, keys, body=True):
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
                raise BadRequestException("Key '%s' contains an invalid "
                                          "boolean value ('%s')." %
                                          (key, event['body'][key]))
        else:
            if key not in event.keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if re.match(r"yes|no", event[key]):
                raise BadRequestException("Key '%s' contains an invalid "
                                          "boolean value ('%s')." %
                                          (key, event[key]))


def _check_decimal(event, keys, body=True):
    """
    Ensure that certain values are a valid Decimal and not a string.
    :param event: The event object from Lambda.
    :param keys: List of keys to test.
    :param body: Check in the body or in the event itself.
    :return: Nothing if success, exception if failed.
    """
    for key in keys:
        if body is True:
            if key not in event['body'].keys():
                raise BadRequestException("Key '%s' is missing." % key)
            try:
                Decimal(event['body'][key])
            except InvalidOperation:
                raise BadRequestException(
                    "Key '%s' contains an invalid decimal value ('%s')." %
                    (key, event['body'][key]))
        else:
            if key not in event.keys():
                raise BadRequestException("Key '%s' is missing." % key)
            try:
                Decimal(event[key])
                return
            except InvalidOperation:
                raise BadRequestException(
                    "Key '%s' contains an invalid decimal value ('%s')." %
                    (key, event[key]))


def _check_duplicate(dynamo_table, table_index, keys, exclude_value=None,
                     exclude_attr='id'):
    """
    Checks for a duplicate entry of the given keys in a given table using a
    given index.
    :param dynamo_table: The Table object to search.
    :param table_index: The name of the index to search in.
    :param keys: Dictionary of the keys needed for the index.
    :param exclude_value: Optional value to exclude from duplicate detection.
    :return: None if Good, Exception if Duplicate.
    """

    try:
        results = dynamo_table.query(IndexName=table_index,
                                     KeyConditionExpression=
                                     _build_key_expression_from_dict(keys))
        # If there is one and only one result, and we were given an exclude id
        # (likely for update) - See if it's the thing we're updating.
        if len(results['Items']) == 1 and exclude_value is not None:
            # The ID needs to match, else it's toast
            if results['Items'][0][exclude_attr] == exclude_value:
                return
        # No results means no duplicates
        if len(results['Items']) == 0:
            return
        # Whelp, you dun goofd Jon Snow
        raise BadRequestException("Duplicate object (Keys:%s) found in table "
                                  "'%s'" % (keys, dynamo_table.table_name))
    except ClientError as ce:
        raise InternalServerException(ce.message)


def test_relation(foreign_table, key, value):
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
        raise NotFoundException("Object '%s' for relation not found in "
                                "table '%s'." %
                                (value, foreign_table.table_name))


def test_relation_attr(foreign_table, foreign_key_attr, foreign_key,
                       foreign_attr, value):
    """
    Check a local value against a given attribute of a specific item
    from another table.

    NOTE: This will choke on more than one result. Might need to implement
    RangeKeys at a later date.

    :param foreign_table: The foreign table object.
    :param foreign_key_attr: The foreign table HashKey attribute.
    :param foreign_key: The key (ID) of an element in the foreign table.
    :param foreign_attr: The attribute in the foreign table to look up.
    :param value: The value to compare against.
    :return: None if good, Exception if bad.
    """

    try:
        response = foreign_table.get_item(Key={foreign_key_attr: foreign_key})
    except ClientError as ce:
        raise InternalServerException(ce.message)

    if 'Item' not in response:
        raise NotFoundException("Object '%s' for relation not found in table "
                                "'%s'." % (value, foreign_table.table_name))

    if response['Item'][foreign_attr] == value:
        return

    raise NotFoundException("Table '%s' with '%s'='%s' does not match on "
                            "attribute '%s' (got '%s')" %
                            (foreign_table.table_name, foreign_key_attr,
                             foreign_key, foreign_attr, value))


def test_types(event):
    """
    Perform data type validation on certain keys.
    :param event: The event to test.
    :return: None if success, Exception if failed.
    """
    _check_boolean(event, BOOLEAN_FIELDS)
    # I'm sure there will be more here some day.


def test_keys(event, mode, required_keys):
    """
    Tests for the presence of required keys in the event.
    :param event: The event to test.
    :param mode: Determines which checks should be performed.
    :param required_keys: List of keys to test for in the event.
    :return: None if success, Exception if failed.
    """
    if mode == MODE_CREATE:
        # We need all of the required keys for this.
        _check_keys(required_keys, event)
    elif mode == MODE_READ or mode == MODE_DELETE:
        # ID is the only field we care about, so ignore the required_keys.
        _check_keys(['pathId'], event, False)
    elif mode == MODE_UPDATE:
        # This requires both ID and a set of keys.
        _check_keys(['pathId'], event, False)
        _check_keys(required_keys, event)
    else:
        # If we get here, something went very wrong.
        raise BadRequestException("Invalid key validation mode specified ('%s')." % mode)