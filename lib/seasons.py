#!/usr/bin/env python
import database
import validation
import decimal
from uuid import uuid4
from lib.tables import SeasonsTable, LeaguesTable
from lib.exceptions import *

# These are the required attributes for this object.
required_keys = ['id', 'is_women', 'league', 'start_year', 'end_year']


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
    return database.create_element(SeasonsTable, event)


def perform_read(event):
    """
    Take the event and use it to read an existing object from the database.
    :param event: The event.
    :return: A JSON blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_READ,
                                     required_keys=required_keys)
    return database.read_element(table=SeasonsTable, event=event)


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
    return database.update_element(SeasonsTable, event, required_keys)


def perform_delete(event):
    """
    Take the event and use it to delete an existing object from the database.
    :param event: The verified event.
    :return: A blob of the object.
    """
    validation.run_event_input_tests(event=event, mode=validation.MODE_DELETE)

    return database.delete_element(table=SeasonsTable, event=event)


def perform_list(event):
    """
    Take the event and use it to list objects from the database.
    :param event: The Lambda event.
    :return: A blob of objects.
    """
    # Query
    league_id = event['league']
    start_year = event['start_year']
    is_women = event['is_women']

    try:
        # You have to use == or Python gets stupid.
        if league_id == "" or start_year == "":
            return database.scan_table(SeasonsTable)
        else:
            # Now find the seasons.
            seasons_query_exp = {
                "league": league_id,
                "start_year": decimal.Decimal(start_year)
            }
            season_results = database.query_table(SeasonsTable, "SeasonByLeagueStart", seasons_query_exp)

            entries = []
            for season in season_results:
                if season['is_women'] == is_women:
                    entries.append(season)

            if len(entries) >= 1:
                # @TODO: This should probably throw an exception for >1
                return entries[0]

            raise NotFoundException("Season starting '%i' not found for league '%s' with is_women='%s'." % (start_year, league_id, is_women))
    except ClientError as ce:
        raise InternalServerException(ce.message)


def perform_list_by_league(event):
    """
    List seasons from the database by a given league.
    :param event: The Lambda event.
    :return: A list of database elements.
    """
    try:
        # Get the Conference objects for this institution.
        seasons_query_exp = {
            "league": event['pathId']
        }
        season_results = database.query_table(SeasonsTable, "SeasonByLeagueGender",
                                              seasons_query_exp)
        return season_results
    except ClientError as ce:
        raise InternalServerException(ce.message)
