#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="PUT"
ENDPOINT="/team/f5b1867f-e43d-4340-9bec-2c1c9b5f5e25"
SUB_ATTR="nickname"
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