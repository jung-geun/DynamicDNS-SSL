#!/bin/bash

export CLOUDFLARE_API_KEY=$API_KEY
export CLOUDFLARE_DOMAIN=$DOMAIN_NAME
export CLOUDFLARE_ZONE_ID=$ZONE_ID

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the script
python3 $DIR/src/update_dns.py $@