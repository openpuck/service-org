#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="GET"
PAYLOAD=''
ENDPOINT="/league/0ea6a113-4ccf-4961-acf0-f39ec91b5a9d"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp