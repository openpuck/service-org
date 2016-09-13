#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="GET"
PAYLOAD=''
ENDPOINT="/00b89928-f9e0-4f8e-a066-4983e02150ec"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp