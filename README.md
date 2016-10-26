Org Service
===========

This service provides organizational information.

## Objects
* Leagues
* Conferences
* Teams
* Seasons
* Institutions

## Structure
* /league (GET, POST)
  * /{id} (GET, PUT, DELETE)
    * /conferences (GET)
    * /seasons (GET)
    * /institutions (GET)
  * /?abbr=LEAGUE_ABBREVIATION
* /conference (GET, POST)
  * /{id} (GET, PUT, DELETE)
    * /teams (GET)
  * /?league_abbr=LEAGUE_ABBREVIATION&conf_abbr=CONFERENCE_ABBREVIATION&is_women=YES_OR_NO
* /team (GET, POST)
  * /{id} (GET, PUT, DELETE)
* /season (GET, POST)
  * /{id} (GET, PUT, DELETE)
* /institution (GET, POST)
  * /{id} (GET, PUT, DELETE)
    * /teams (GET)
    * /leagues (GET)

TODO
* Docs for query

## Function Pattern
### Lambda Handler
Small skeleton code that essentially does a few things:
1) Instantiates the object type based on that context.
2) Calls the appropriate perform_operation (ex: `perform_create()`)
3) Returns the output as a JSON blob.

### Object Type
Collection of functions to perform operations on a specific context.

Database functions for each operation should be implemented (ex: `perform_create()`). These will call any context-specific validation functions such as `perform_input_tests()` and `test_relations()`.

### Database Library
Lowest-level application-specific database operations. Implements certain type and data validation. Mostly exists for the (ex) `create_element()` functions and actually interact with the DB.

## Development Dependencies
* NodeJS 4.X
* Serverless 0.4.2
* bash, curl, jq, perl

## References
Old scripts are at [the old repo](https://github.com/cohoe/OpenPuck/tree/45160b6e6987a6de2563b4bfd8b9e143553ea79c)