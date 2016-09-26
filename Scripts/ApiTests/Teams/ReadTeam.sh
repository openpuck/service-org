#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="GET"
PAYLOAD=''
ENDPOINT="/team/39162250-c85b-438d-a6ac-79e110f11c22"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp