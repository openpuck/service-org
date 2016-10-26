#!/usr/bin/env python
import database
import validation
from uuid import uuid4
from lib.tables import LeaguesTable, ConferencesTable, TeamsTable
from lib.exceptions import *

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
        validation.test_keys(event, mode, required_keys)
        validation.test_types(event)
        test_relations(event)
    elif mode == validation.MODE_READ:
        validation.test_keys(event, mode, required_keys)
    elif mode == validation.MODE_DELETE:
        # @TODO: Test for delete
        pass
    else:
        # If we get here, something went very wrong.
        raise BadRequestException("Invalid input test validation mode "
                                  "specified ('%s')." % mode)


def test_relations(event):
    """
    Tests for appropriate relations for the given event.
    :param event: The event to test.
    :return: None if success, Exception if failed.
    """
    validation.test_relation(LeaguesTable, 'id',
                             event['body']['league'])
    validation.test_relation(ConferencesTable, 'id',
                             event['body']['conference'])
    validation.test_relation_attr(ConferencesTable, 'id',
                                  event['body']['conference'], 'is_women',
                                  event['body']['is_women'])
    validation.test_relation_attr(ConferencesTable, 'id',
                                  event['body']['conference'], 'league',
                                  event['body']['league'])


def perform_create(event):
    """
    Take the event and use it to create a new object in the database.
    :param event: The event.
    :return: A blob of the new object.
    """
    # Jam in an ID for the new object.
    event['body']['id'] = str(uuid4())

    perform_input_tests(event, mode=validation.MODE_CREATE)
    return database.create_element(TeamsTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The event.
    :return: A JSON blob of the object.
    """
    perform_input_tests(event, mode=validation.MODE_READ)
    return database.read_element(table=TeamsTable, event=event)


def perform_update(event):
    """
    Take the event and use it to update an existing object in the database.
    :param event: The event.
    :return: A blob of the updated object.
    """
    perform_input_tests(event, mode=validation.MODE_UPDATE)
    return database.update_element(table=TeamsTable, event=event,
                                   keys=required_keys)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A blob of the object.
    """
    perform_input_tests(event, mode=validation.MODE_DELETE)
    return database.delete_element(table=TeamsTable, event=event)


def perform_list(event):
    """
    Take the event and use it to list objects from the database.
    :param event: The Lambda event.
    :return: A blob of objects.
    """
    try:
        # You have to use == or Python gets stupid.
        if event['institution'] == "" or event['is_women'] == "":
            return database.scan_table(TeamsTable)
        else:
            key_expression_dict = {
                "institution": event['institution'],
                "is_women": event['is_women']
            }

            return database.query_table(TeamsTable, "TeamsByInstitutionGender",
                                        key_expression_dict)
    except ClientError as ce:
        raise InternalServerException(ce.message)
