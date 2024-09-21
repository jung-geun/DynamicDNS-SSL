#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -f $DIR/../config/env.json ]; then
    cp $DIR/../config/default_env.json $DIR/../config/env.json
fi

$DIR/run_script.sh

tail -f /var/log/cloudflare_ddns.log