#!/bin/bash

set -e

# Load in our common stuff.
source Common.sh

# Test Harness
test_function() {
    local function_name=$1
    echoerr "Testing function ${function_name}..."
    echo $(${function_name})
    sleep 1
    echoerr "Done"
    echoerr ""
    sleep 1
}

# Run tests
test_function "get_test_league_id"
test_function "get_test_conference_id"
test_function "get_test_season_id"
test_function "get_test_institution_id"
test_function "get_test_team_id"