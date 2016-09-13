#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="DELETE"
PAYLOAD=''
ENDPOINT="/league/883c9dbf-5aae-400e-8110-84b68cee6838"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp