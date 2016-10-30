#!/usr/bin/env python
import database
import validation
from uuid import uuid4
from lib.tables import LeaguesTable, ConferencesTable, TeamsTable
from lib.exceptions import *

# These are the required attributes for this object.
required_keys = ['nickname', 'institution', 'provider', 'is_women',
                 'league', 'conference', 'is_active', 'website']


def _build_relations(event):
    """
    Build a list of relations that need to be tested.
    :param event: The event.
    :return: A list of dictionary relations.
    """
    relations = [
        {
            "table": LeaguesTable,
            "key": "id",
            "value": event['body']['league']
        },
        {
            "table": ConferencesTable,
            "key": "id",
            "value": event['body']['conference']
        },
        {
            "table": ConferencesTable,
            "key": "id",
            "value": event['body']['conference'],
            "foreign_key": "is_women",
            "foreign_value": event['body']['is_women']
        },
        {
            "table": ConferencesTable,
            "key": "id",
            "value": event['body']['conference'],
            "foreign_key": "league",
            "foreign_value": event['body']['league']
        },

    ]

    return relations


def _build_duplicates(event, mode):
    """
    Build a list of duplicates that need to be tested.
    :param event: The event.
    :param mode: The current operation mode.
    :return: A list of dictionary duplicates.
    """
    # These set the exclusion parameters for an UPDATE operation. Otherwise
    # the duplication tests will detect itself and choke.
    exclude_value = None
    exclude_attr = 'id'
    if mode == validation.MODE_UPDATE:
        exclude_value = event['pathId']

    # This is a list of dictionaries.
    duplicates = []

    # We good
    return duplicates


def perform_create(event):
    """
    Take the event and use it to create a new object in the database.
    :param event: The event.
    :return: A blob of the new object.
    """
    # Jam in an ID for the new object.
    event['body']['id'] = str(uuid4())

    validation.run_event_input_tests(event=event, mode=validation.MODE_CREATE,
                                     required_keys=required_keys,
                                     relations=_build_relations(event),
                                     duplicates=_build_duplicates(event,
                                                                  validation.MODE_CREATE))
    return database.create_element(TeamsTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The event.
    :return: A JSON blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_READ,
                                     required_keys=required_keys)
    return database.read_element(table=TeamsTable, event=event)


def perform_update(event):
    """
    Take the event and use it to update an existing object in the database.
    :param event: The event.
    :return: A blob of the updated object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_UPDATE,
                                     required_keys=required_keys,
                                     relations=_build_relations(event),
                                     duplicates=_build_duplicates(event,
                                                                  validation.MODE_UPDATE))
    return database.update_element(table=TeamsTable, event=event,
                                   keys=required_keys)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_DELETE)
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


def perform_list_by_institution(event):
    """
    List teams from the database by a given institution.
    :param event: The Lambda event.
    :return: A list of database elements.
    """
    try:
        # Get the Team objects for this institution.
        teams_query_exp = {
            "institution": event['pathId']
        }
        team_results = database.query_table(TeamsTable, "TeamsByInstitutionGender",
                                            teams_query_exp)
        return team_results
    except ClientError as ce:
        raise InternalServerException(ce.message)


def perform_list_by_conference(event):
    """
    List teams from the database by a given conference.
    :param event: The Lambda event.
    :return: A list of database elements.
    """
    try:
        # Get the Team objects for this institution.
        teams_query_exp = {
            "conference": event['pathId']
        }
        team_results = database.query_table(TeamsTable, "TeamsByConference",
                                            teams_query_exp)
        return team_results
    except ClientError as ce:
        raise InternalServerException(ce.message)
