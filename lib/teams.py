#!/usr/bin/env python
import validation
from uuid import uuid4
from lib.tables import LeaguesTable, ConferencesTable, TeamsTable
from lib import create_database_element, update_database_element

# These are the required attributes for this object.
required_keys = ['nickname', 'institution', 'provider', 'is_women',
                 'league', 'conference', 'is_active', 'website']


def perform_input_tests(event, update_mode=True):
    """
    Metafunction to run the standard set of tests against the given event.
    :param event: The event to test.
    :param update_mode: Whether this is an Update (True) or Create (False).
    :return: None if success, Exception if failed.
    """
    test_keys(event, update_mode)
    test_validation(event)
    test_relations(event)


def test_keys(event, update_mode=True):
    # @TODO: Move this to validation and make generic
    """
    Tests for the presence of required keys in the event.
    :param event: The event to test.
    :param update_mode: Whether this is an Update (True) or Create (False)
    :return: None if success, Exception if failed.
    """
    if update_mode is True:
        validation.check_keys(['pathId'], event, False)
    validation.check_keys(required_keys, event)


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
