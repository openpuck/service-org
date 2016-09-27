#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="DELETE"
PAYLOAD=''
ENDPOINT="/season/c33f5d78-34db-4ee4-aa63-1d8c9997adc2"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp