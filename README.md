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

TODO
* /league/{id}/conferences (POST)
* /league/{id}/conferences/{id} (DELETE)
* /league/{id}/seasons (POST)
* /league/{id}/seasons/{id} (DELETE)
* /conference/{id}/teams (POST)
* /conference/{id}/teams/{id} (DELETE)
* /institution/{id}/teams (GET)
* /institution/{id}/leagues (GET)
* /league/{id}/institutions (GET)

## Development Dependencies
* NodeJS 4.X
* Serverless 0.4.2
* bash, curl, jq, perl

## References
Old scripts are at [the old repo](https://github.com/cohoe/OpenPuck/tree/45160b6e6987a6de2563b4bfd8b9e143553ea79c)