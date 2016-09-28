#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/conference?league_abbr=${TEST_LEAGUE_ABBR}\&conf_abbr=${TEST_CONFERENCE_ABBR}\&is_women=${TEST_CONFERENCE_IS_WOMEN}"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"