#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/season?league=$(get_test_league_id)&start_year=${TEST_SEASON_START_YEAR}&is_women=${TEST_SEASON_IS_WOMEN}"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"