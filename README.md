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

## Development Dependencies
* NodeJS 4.X
* Serverless 0.4.2
* bash, curl, jq, perl

## References
Old scripts are at [the old repo](https://github.com/cohoe/OpenPuck/tree/45160b6e6987a6de2563b4bfd8b9e143553ea79c)