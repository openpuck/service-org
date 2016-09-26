#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars

METHOD="POST"
PAYLOAD='{
"nickname": "Centurions",
"institution": "Cylons",
"provider": "SidearmAdaptiveProvider",
"is_women": "yes",
"league": "ac99003b-845d-4cec-9c02-4dfe1acc1839",
"conference": "f550d8ed-bc80-407a-be09-ee1b85ba3bca",
"is_active": "yes",
"website": "http://foo"
}'
ENDPOINT="/team"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp