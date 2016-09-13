#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="GET"
PAYLOAD=''
ENDPOINT="/league"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp