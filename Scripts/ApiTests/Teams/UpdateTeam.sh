#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="PUT"
ENDPOINT="/team/f5b1867f-e43d-4340-9bec-2c1c9b5f5e25"

# Execute
#echo "${URL}/${ENDPOINT}"
output=$(${CURL} -X "GET" ${URL}${ENDPOINT})
echo "EXISTING: $output"
PAYLOAD=$(echo $output | perl -pe "s|\"is_women\": \"(.*?)\"|\"is_women\": \"$(date)\"|")
echo "NEW:      $PAYLOAD"
echo "Updating..."
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp