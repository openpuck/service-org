#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="PUT"
ENDPOINT="/conference/c3a2f13e-f025-401e-99f4-7c33fe64708d"
SUB_ATTR="abbr"
SUB_VALUE=$(date)

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