#!/bin/bash

URL=https://mkvusbh1l7.execute-api.us-east-1.amazonaws.com/dev/league

curl -s $URL | json_pp