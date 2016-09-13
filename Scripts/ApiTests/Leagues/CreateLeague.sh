#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
METHOD="POST"
PAYLOAD='{"abbr": "FOOBAR", "cn": "foobar", "website": "lolz"}'
ENDPOINT=""

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp