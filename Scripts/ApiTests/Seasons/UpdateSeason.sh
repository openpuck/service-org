#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="PUT"
ENDPOINT="/season/ceb73d9a-86ee-4ab7-a9da-bb78769fc584"
SUB_ATTR="start"
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