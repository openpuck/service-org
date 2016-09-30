#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars

METHOD="POST"
PAYLOAD='{
"is_women": "yes",
"league": "ac99003b-845d-4cec-9c02-4dfe1acc1839",
"start_year": "2016",
"end_year": "2017"
}'
ENDPOINT="/season"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp

#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/season"
METHOD="POST"

# Payload
read -d '' PAYLOAD << EndOfPayload
{
"is_women": "yes",
"league": "$(get_league_id)",
"start_year": "2016",
"end_year": "2017"
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"