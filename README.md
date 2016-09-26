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
* /conference (GET, POST)
  * /{id} (GET, PUT, DELETE)
    * /teams (GET, POST)
      * /teams/{id} (GET, DELETE)
* /team (GET, POST)
  * /{id} (GET, PUT, DELETE)

TODO
* /league/{id}/seasons (GET)
* /season (GET, POST)
  * /{id} (GET, PUT, DELETE)
* /institution (GET, POST)
  * /{id} (GET, PUT, DELETE)
    * /teams (GET)
    * /leagues (GET)

## References
Old scripts are at [the old repo](https://github.com/cohoe/OpenPuck/tree/45160b6e6987a6de2563b4bfd8b9e143553ea79c)