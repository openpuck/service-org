#!/bin/bash

URL=https://mkvusbh1l7.execute-api.us-east-1.amazonaws.com/dev/league/ac99003b-845d-4cec-9c02-4dfe1acc1839

curl -s $URL | json_pp