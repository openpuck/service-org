#!/usr/bin/env python
import database
import validation
from uuid import uuid4
from lib.tables import LeaguesTable, TeamsTable
from lib.exceptions import *

# These are the required attributes for this object.
required_keys = ['abbr', 'cn', 'website']


def _build_relations(event):
    """
    Build a list of relations that need to be tested.
    :param event: The event.
    :return: A list of dictionary relations.
    """
    relations = []

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
    exclude_attr = 'abbr'
    if mode == validation.MODE_UPDATE:
        exclude_value = event['body']['abbr']

    # This is a list of dictionaries.
    duplicates = [
        {
            "table": LeaguesTable,
            "index": 'AbbrIndex',
            "keys": {
                'abbr': event['body']['abbr']
            },
            "exclude_attr": exclude_attr,
            "exclude_value": exclude_value
        }
    ]

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
                                     duplicates=_build_duplicates(event, validation.MODE_CREATE))
    return database.create_element(LeaguesTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The event.
    :return: A JSON blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_READ,
                                     required_keys=required_keys)
    return database.read_element(table=LeaguesTable, event=event)


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
    return database.update_element(LeaguesTable, event, required_keys)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_DELETE)

    return database.delete_element(table=LeaguesTable, event=event)


def perform_list(event):
    """
    Take the event and use it to list objects from the database.
    :param event: The Lambda event.
    :return: A blob of objects.
    """
    # Query
    search_abbr = event['abbr']

    try:
        # You have to use == or Python gets stupid.
        if search_abbr == "":
            return database.scan_table(LeaguesTable)
        else:
            # Query for the leagues matching the abbr given.
            leagues_query_exp = {
                "abbr": search_abbr
            }
            league_results = database.query_table(LeaguesTable, "AbbrIndex", leagues_query_exp)

            if len(league_results) >= 1:
                # @TODO: This should probably throw an exception.
                return league_results

            return []
            # raise NotFoundException("Abbreviated league '%s' not found." % search_abbr)
    except ClientError as ce:
        raise InternalServerException(ce.message)


def perform_list_by_institution(event):
    """
    Take the event and use it to list leagues from the database by a given
    institution.
    :param event: The Lambda event.
    :return: A list of database elements.
    """
    try:
        leagues = []

        # We first must get the Team objects for this institution.
        teams_query_exp = {
            "institution": event['pathId']
        }
        team_results = database.query_table(TeamsTable, "TeamsByInstitutionGender", teams_query_exp)

        # Foreach team, grab it's league object
        for team in team_results:
            league_event = {"pathId": team['league']}
            league_result = database.read_element(LeaguesTable, league_event)

            # Check if the league is already there
            if not leagues:
                leagues.append(league_result)
            else:
                for league in leagues:
                    if league['id'] != league_result['id']:
                        leagues.append(league_result)
        # Done
        return leagues
    except ClientError as ce:
        raise InternalServerException(ce.message)
