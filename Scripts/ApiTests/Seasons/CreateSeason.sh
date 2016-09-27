#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars

METHOD="POST"
PAYLOAD='{
"is_women": "yes",
"league": "ac99003b-845d-4cec-9c02-4dfe1acc1839",
"start": "2016",
"end": "2017"
}'
ENDPOINT="/season"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp