#!/bin/bash

# Test Vars
TEST_CONFERENCE_ABBR="FOOBAR"
TEST_LEAGUE_ABBR="NCAA"

# Environment
DEBUG=0
if [[ ${DEBUG} == 1 ]]; then
    DEBUG_OPTS="-v"
else
    DEBUG_OPTS=""
fi

# Common Stuff
URL="https://mkvusbh1l7.execute-api.us-east-1.amazonaws.com/dev"
CURL="curl -s ${DEBUG_OPTS} -H 'Content-Type: application/json'"

# Functions
perform_call() {
    # Make a curl call for our testing

    # Local variables
    local METHOD=$1
    local URL=$2
    local ENDPOINT=$3
    local PAYLOAD=$4

    # Generate and run the call.
    command_string="${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d '${PAYLOAD}'"
    data=$(eval ${command_string})

    # Return the output.
    echo ${data} | json_pp
}
get_league_id() {
    # Return the id of our test league from the API so we can do easy lookups
    # with it in other functions.
    local endpoint="/league?abbr=${TEST_LEAGUE_ABBR}"
    local league=$(perform_call "GET" ${URL} ${endpoint} "")
    echo ${league} | jq -r '.id'
}