#!/usr/bin/env python
import database
import validation
from uuid import uuid4
from lib.tables import LeaguesTable, ConferencesTable
from lib.exceptions import *

# These are the required attributes for this object.
required_keys = ['cn', 'is_women', 'abbr', 'website', 'league']


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
        }
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
    duplicates = [
        {
            "table": ConferencesTable,
            "index": 'ConfByAbbrGender',
            "keys": {
                'abbr': event['body']['abbr'],
                'is_women': event['body']['is_women']
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
    return database.create_element(ConferencesTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The event.
    :return: A JSON blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_READ,
                                     required_keys=required_keys)
    return database.read_element(table=ConferencesTable, event=event)


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
    return database.update_element(ConferencesTable, event, required_keys)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_DELETE)

    return database.delete_element(table=ConferencesTable, event=event)


def perform_list(event):
    """
    Take the event and use it to list objects from the database.
    :param event: The Lambda event.
    :return: A blob of objects.
    """
    # Query
    league_abbr = event['league_abbr']
    conf_abbr = event['conf_abbr']
    is_women = event['is_women']

    try:
        # You have to use == or Python gets stupid.
        if league_abbr == "" or conf_abbr == "" or is_women == "":
            return database.scan_table(ConferencesTable)
        else:
            # Query for the leagues matching the abbr given.
            leagues_query_exp = {
                "abbr": league_abbr
            }
            league_results = database.query_table(LeaguesTable, "AbbrIndex", leagues_query_exp)

            # Now find the conference.
            for league in league_results:
                conf_query_exp = {
                    "league": league['id']
                }
                conf_results = database.query_table(ConferencesTable, "ConfByLeagueGender", conf_query_exp)

                entries = []
                for conf in conf_results:
                    if conf['abbr'] == conf_abbr and conf['is_women'] == is_women:
                        entries.append(conf)

                # We will only return the first one if there are more.
                # @TODO This might need to be an exception.
                if len(entries) >= 1:
                    return entries

                # raise NotFoundException("Conference '%s' not found for league '%s' with is_women='%s'." % (conf_abbr, league_abbr, is_women))
                return []
            # return lib.get_json(league_result['Items'])
    except ClientError as ce:
        raise InternalServerException(ce.message)


def perform_list_by_league(event):
    """
    List conferences from the database by a given league.
    :param event: The Lambda event.
    :return: A list of database elements.
    """
    try:
        # Get the Conference objects for this institution.
        conferences_query_exp = {
            "league": event['pathId']
        }
        conference_results = database.query_table(ConferencesTable, "ConfByLeagueGender",
                                                  conferences_query_exp)
        return conference_results
    except ClientError as ce:
        raise InternalServerException(ce.message)
