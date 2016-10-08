#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/league/$(get_league_id)/institutions"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"