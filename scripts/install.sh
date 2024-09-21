#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

@echo off
echo "Certbot and Cloudflare API tools installation"
sudo apt update
sudo apt install -y certbot python3-certbot-dns-cloudflare jq

sudo mkdir -p /app/cloudflare-ddns
sudo cp -r $DIR/../* /app/cloudflare-ddns
if [ -f /app/cloudflare-ddns/config/env.json ]; then
  echo "Environment configuration file already exists. Back up the existing file and create a new file."
  sudo mv /app/cloudflare-ddns/config/env.json /app/cloudflare-ddns/config/env.json.bak
fi
sudo mkdir -p /app/cloudflare-ddns/config
sudo cp $DIR/../config/env_example.json /app/cloudflare-ddns/config/env.json
sudo chmod 600 /app/cloudflare-ddns/config/env.json
sudo cp $DIR/../cron/cronjob-ddns /etc/cron.d/cloudflare-ddns
echo "Please modify the environment configuration file and save it in the /app/cloudflare-ddns/config/env.json path."

echo "Certbot and Cloudflare API tools installation completed."