#!/usr/bin/env python
import database
import validation
from uuid import uuid4
from lib.tables import InstitutionsTable, TeamsTable
from lib.exceptions import *

# These are the required attributes for this object.
required_keys = ['cn', 'city']


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
                                     duplicates=_build_duplicates(event, validation.MODE_CREATE))
    return database.create_element(InstitutionsTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The event.
    :return: A JSON blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_READ,
                                     required_keys=required_keys)
    return database.read_element(table=InstitutionsTable, event=event)


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
    return database.update_element(InstitutionsTable, event, required_keys)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_DELETE)

    return database.delete_element(table=InstitutionsTable, event=event)


def perform_list(event):
    """
    Take the event and use it to list objects from the database.
    :param event: The Lambda event.
    :return: A blob of objects.
    """
    # Query
    search_cn = event['cn']

    try:
        # You have to use == or Python gets stupid.
        if search_cn == "":
            return database.scan_table(InstitutionsTable)
        else:
            # Search for the institution we're after
            # @TODO: It would be nice to not have to scan all of the things.
            institutions = database.scan_table(InstitutionsTable)
            entries = []
            for institution in institutions:
                if institution['cn'] == search_cn:
                    entries.append(institution)
            if len(entries) >= 1:
                # @TODO: This should probably throw an exception for >1.
                return entries[0]

            raise NotFoundException("Institution '%s' not found." % search_cn)

    except ClientError as ce:
        raise InternalServerException(ce.message)


def perform_list_by_league(event):
    """
    List conferences from the database by a given league.
    :param event: The Lambda event.
    :return: A list of database elements.
    """
    try:
        institutions = []

        # We first must get the Team objects for this institution.
        teams_query_exp = {
            "league": event['pathId']
        }
        team_results = database.query_table(TeamsTable,
                                            "TeamsByLeagueGender",
                                            teams_query_exp)

        # Foreach team, grab it's institution object
        for team in team_results:
            institution_event = {"pathId": team['institution']}
            institution_result = database.read_element(InstitutionsTable, institution_event)

            # Check if the institution is already there
            if not institutions:
                institutions.append(institution_result)
            else:
                for institution in institutions:
                    if institution['id'] != institution_result['id']:
                        institutions.append(institution_result)
        # Done
        return institutions
    except ClientError as ce:
        raise InternalServerException(ce.message)