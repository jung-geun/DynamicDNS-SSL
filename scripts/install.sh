#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo -e "Certbot and Cloudflare API tools installation started. \n"
sudo apt -qq update
PKG_LIST=(certbot python3-certbot-dns-cloudflare jq)
for pkg in ${PKG_LIST[@]}; do
  dpkg -l | grep -q $pkg
  if [ $? -eq 0 ]; then
    echo "$pkg is already installed."
    read -p "Do you want to reinstall it? (y/N): " reinstall
    reinstall=${reinstall:-n}
    if [ "$reinstall" == "y" ]; then
      sudo apt install --reinstall -y $pkg
    fi
    echo -e "\n\n"
  else
    echo "$pkg is not installed."
    sudo apt install -y $pkg
  fi
done

sudo mkdir -p /app/cloudflare-ddns
sudo cp -r $DIR/../* /app/cloudflare-ddns
if [ -f /app/cloudflare-ddns/config/env.json ]; then
  read -p "Environment configuration file already exists. Do you want to overwrite it? (y/N): " overwrite
  overwrite=${overwrite:-n}
  if [ "$overwrite" == "y" ]; then
    sudo mv /app/cloudflare-ddns/config/env.json /app/cloudflare-ddns/config/env.json.bak
    sudo cp $DIR/../config/env_example.json /app/cloudflare-ddns/config/env.json
    sudo chmod 600 /app/cloudflare-ddns/config/env.json
  else
    echo -e "Environment configuration file is not overwritten. \n"
  fi
else
  sudo mkdir -p /app/cloudflare-ddns/config
  sudo cp $DIR/../config/env_example.json /app/cloudflare-ddns/config/env.json
  sudo chmod 600 /app/cloudflare-ddns/config/env.json
fi
sudo cp $DIR/../cron/cronjob-ddns /etc/cron.d/cloudflare-ddns
echo -e "Please modify the environment configuration file and save it in the /app/cloudflare-ddns/config/env.json path. \n"

echo -e "Certbot and Cloudflare API tools installation completed. \n"