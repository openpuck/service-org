#!/bin/bash

#set -e

# Test Vars
TEST_CONFERENCE_ABBR="FOOBAR"
TEST_CONFERENCE_IS_WOMEN="yes"
TEST_LEAGUE_ABBR="NCAA"
TEST_SEASON_START_YEAR=2015
TEST_SEASON_IS_WOMEN="yes"
TEST_INSTITUTION_CN="FOOBAR INSTITUTE OF TECHNOLOGY"

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
echoerr() {
    # Echo something to stderr
    >&2 echo $1 $2
}

perform_call() {
    # Make a curl call for our testing

    # Local variables
    local METHOD=$1
    local URL=$2
    local ENDPOINT=$3
    local PAYLOAD=$4
    local NO_PRETTY=$5

    # Generate and run the call.
    command_string="${CURL} -X ${METHOD} \"${URL}${ENDPOINT}\" -d '${PAYLOAD}'"
    echoerr "Command String:" "${command_string}"
    data=$(eval ${command_string})

    # Return the output.
    if [ -n "${NO_PRETTY}" ]; then
        echo ${data}
    else
        echo ${data} | json_pp
    fi
}

sub_payload() {
    # Substitute a given attribute's value for something new in a string.
    local output=$1
    local SUB_ATTR=$2
    local SUB_VALUE=$3

    # Thanks internet! http://stackoverflow.com/questions/1103149/non-greedy-regex-matching-in-sed
    local PAYLOAD=$(echo ${output} | perl -pe "s|\"${SUB_ATTR}\": \"(.*?)\"|\"${SUB_ATTR}\": \"${SUB_VALUE}\"|")
    echo ${PAYLOAD}
}
get_league_id() {
    # Return the id of our test league from the API so we can do easy lookups
    # with it in other functions.
#    echoerr "BEGIN get-league_id"
    local endpoint="/league?abbr=${TEST_LEAGUE_ABBR}"
    local league=$(perform_call "GET" ${URL} ${endpoint} "")
    local league_id=$(echo ${league} | jq -r '.id')
#    echoerr "League ID:" "${league_id}"
    echo ${league_id}
#    echoerr "END get-league_id"
}

get_conference_id() {
    # Return the id of our test conference from the API so we can do easy lookups
    # with it in other functions.
    local endpoint="/conference?league_abbr=${TEST_LEAGUE_ABBR}&conf_abbr=${TEST_CONFERENCE_ABBR}&is_women=${TEST_CONFERENCE_IS_WOMEN}"
    local conference=$(perform_call "GET" ${URL} ${endpoint} "")
    local conference_id=$(echo ${conference} | jq -r '.id')
    echoerr "Conference ID:" "${conference_id}"
    echo ${conference_id}
}

get_season_id() {
    # Return the id of our test season.
    local endpoint="/season?league=$(get_league_id)&start_year=${TEST_SEASON_START_YEAR}&is_women=${TEST_SEASON_IS_WOMEN}"
    local season=$(perform_call "GET" ${URL} ${endpoint} "")
    local season_id=$(echo ${season} | jq -r '.id')
    echoerr "Season ID:" "${season_id}"
    echo ${season_id}
}

get_institution_id() {
    # Return the id of our test institution.
    local endpoint="/institution?cn=$(urlencode "${TEST_INSTITUTION_CN}")"
    local institution=$(perform_call "GET" ${URL} ${endpoint} "")
    local institution_id=$(echo ${institution} | jq -r '.[].id')
    echoerr "Institution ID:" "${institution_id}"
    echo ${institution_id}
}

urlencode() {
    # Return an urlencoded version of a string.
    local inputstring=$1

    echoerr "Input String: ${inputstring}"

    # Thanks internet! http://stackoverflow.com/questions/296536/how-to-urlencode-data-for-curl-command
#    local PAYLOAD=$(echo ${output} | perl -pe "s|\"${SUB_ATTR}\": \"(.*?)\"|\"${SUB_ATTR}\": \"${SUB_VALUE}\"|")
    local PAYLOAD=$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "${inputstring}")
    echo ${PAYLOAD}
}