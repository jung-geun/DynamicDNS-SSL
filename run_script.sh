#!/bin/bash
export CLOUDFLARE_API_KEY=$API_KEY
export CLOUDFLARE_DOMAIN=$DOMAIN_NAME
export CLOUDFLARE_ZONE_ID=$ZONE_ID

# Run the script
python3 /app/cloudflare-ddns/src/update_dns.py $@