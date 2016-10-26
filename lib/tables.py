#!/usr/bin/env python

import lib

LeaguesTable = lib.database.get_table(lib.database.LEAGUES_TABLE)
TeamsTable = lib.database.get_table(lib.database.TEAMS_TABLE)
ConferencesTable = lib.database.get_table(lib.database.CONFERENCES_TABLE)
InstitutionsTable = lib.database.get_table(lib.database.INSTITUTIONS_TABLE)
SeasonsTable = lib.database.get_table(lib.database.SEASONS_TABLE)
