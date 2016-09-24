#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="GET"
PAYLOAD=''
ENDPOINT="/conference/c3a2f13e-f025-401e-99f4-7c33fe64708d"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp