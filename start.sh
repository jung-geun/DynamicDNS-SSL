#!/bin/bash
if [ ! -f /app/cloudflare-ddns/config/env.json ]; then
    cp /app/cloudflare-ddns/init/default_env.json /app/cloudflare-ddns/config/env.json
fi

sh /app/cloudflare-ddns/run_script.sh

# tail -f /var/log/cloudflare_ddns.log