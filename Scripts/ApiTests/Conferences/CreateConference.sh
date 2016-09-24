#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars

METHOD="POST"
PAYLOAD='{"abbr": "FOOBAR", "cn": "foobar", "website": "lolz", "is_women": "yes", "league": "foobar"}'
ENDPOINT="/conference"

# Execute
#echo "${URL}/${ENDPOINT}"
eval ${CURL} -X ${METHOD} ${URL}${ENDPOINT} -d \'${PAYLOAD}\' | json_pp