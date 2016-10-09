#!/usr/bin/env python
import validation
from uuid import uuid4
from lib.tables import LeaguesTable, ConferencesTable, TeamsTable
from lib import create_database_element, update_database_element, read_database_element, delete_database_element
from lib.exceptions import BadRequestException


# These are the required attributes for this object.
required_keys = ['nickname', 'institution', 'provider', 'is_women',
                 'league', 'conference', 'is_active', 'website']


def perform_input_tests(event, mode):
    """
    Metafunction to run the standard set of tests against the given event.
    :param event: The event to test.
    :param mode: Determines which checks should be performed.
    :return: None if success, Exception if failed.
    """
    if mode == validation.MODE_CREATE or mode == validation.MODE_UPDATE:
        test_keys(event, mode)
        test_validation(event)
        test_relations(event)
    elif mode == validation.MODE_READ:
        test_keys(event, mode)
    elif mode == validation.MODE_DELETE:
        # @TODO: Test for delete
        pass
    else:
        # If we get here, something went very wrong.
        raise BadRequestException("Invalid input test validation mode specified ('%s')." % mode)


def test_keys(event, mode):
    # @TODO: Move this to validation and make generic
    """
    Tests for the presence of required keys in the event.
    :param event: The event to test.
    :param mode: Determines which checks should be performed.
    :return: None if success, Exception if failed.
    """
    if mode == validation.MODE_CREATE:
        validation.check_keys(required_keys, event)
    elif mode == validation.MODE_READ or mode == validation.MODE_DELETE:
        validation.check_keys(['pathId'], event, False)
    elif mode == validation.MODE_UPDATE:
        validation.check_keys(['pathId'], event, False)
        validation.check_keys(required_keys, event)
    else:
        # If we get here, something went very wrong.
        raise BadRequestException("Invalid key validation mode specified ('%s')." % mode)


def test_validation(event):
    # @TODO: Move this to validation and make generic.
    """
    Perform data type validation on certain keys.
    :param event: The event to test.
    :return: None if success, Exception if failed.
    """
    validation.check_boolean(event, ['is_women', 'is_active'])


def test_relations(event):
    """
    Tests for appropriate relations for the given event.
    :param event: The event to test.
    :return: None if success, Exception if failed.
    """
    validation.check_relation(LeaguesTable, 'id',
                                  event['body']['league'])
    validation.check_relation(ConferencesTable, 'id',
                                  event['body']['conference'])
    validation.check_relation_attr(ConferencesTable, 'id',
                                       event['body']['conference'], 'is_women',
                                       event['body']['is_women'])
    validation.check_relation_attr(ConferencesTable, 'id',
                                       event['body']['conference'], 'league',
                                       event['body']['league'])


def perform_update(event):
    """
    Take the event and use it to update an existing object in the database.
    :param event: The verified event.
    :return: A JSON blob of the updated object.
    """
    return update_database_element(table=TeamsTable, event=event, keys=required_keys)


def perform_create(event):
    """
    Take the event and use it to create a new object in the database.
    :param event: The verified event.
    :return: A JSON blob of the new object.
    """
    # Jam in an ID for the new object.
    event['body']['id'] = str(uuid4())

    return create_database_element(TeamsTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The verified event.
    :return: A JSON blob of the object.
    """
    return read_database_element(table=TeamsTable, event=event)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A JSON blob of the object.
    """
    return delete_database_element(table=TeamsTable, event=event)
