import re
from lib.exceptions import *
from decimal import Decimal, InvalidOperation


def string_length(input_string, num_chars):
    """
    Check that a given string is of the given length.
    :param input_string: The string to test.
    :param num_chars: The number of characters that should be in that string.
    :return: None if success, Exception if failed.
    """
    if len(input_string) > num_chars:
        raise BadRequestException("Value '%s' has too many characters "
                                  "(max: %d)." % (input_string, num_chars))


def check_keys(keys, event, body=True):
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


def check_decimal(event, keys, body=True):
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
        raise NotFoundException("Object '%s' for relation not found in "
                                "table '%s'." %
                                (value, foreign_table.table_name))


def check_relation_attr(foreign_table, foreign_key_attr, foreign_key,
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
