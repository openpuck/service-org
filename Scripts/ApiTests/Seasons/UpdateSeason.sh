#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="PUT"
ENDPOINT="/season/d120b515-2f87-4773-8856-3f09e71b3d1d"
SUB_ATTR="start_year"
SUB_VALUE=2015

# Existing Object
output=$(${CURL} -X "GET" ${URL}${ENDPOINT})
echo "EXISTING: $output"

# New Object
# Thanks internet! http://stackoverflow.com/questions/1103149/non-greedy-regex-matching-in-sed
PAYLOAD=$(echo $output | perl -pe "s|\"${SUB_ATTR}\": \"(.*?)\"|\"${SUB_ATTR}\": \"${SUB_VALUE}\"|")
echo "NEW:      $PAYLOAD"

# Update
echo "Updating..."
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp