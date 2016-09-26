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
* /conference (GET, POST)
  * /{id} (GET, PUT, DELETE)
    * /teams (GET, POST)
      * /teams/{id} (GET, DELETE)
* /season (GET, POST)
  * /{id} (GET, PUT, DELETE)

## References
Old scripts are at [the old repo](https://github.com/cohoe/OpenPuck/tree/45160b6e6987a6de2563b4bfd8b9e143553ea79c)