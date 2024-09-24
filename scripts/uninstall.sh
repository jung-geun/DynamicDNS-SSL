#!/bin/bash

echo "Uninstalling Cloudflare DDNS and Certbot..."

read -p "Do you want to uninstall Certbot and Cloudflare API tools? (y/N): " uninstall
uninstall=${uninstall:-n}
echo -e "\n"
if [ "$uninstall" == "y" ]; then
    echo "Uninstalling Certbot and Cloudflare API tools..."
    sudo apt remove --purge -y certbot python3-certbot-dns-cloudflare jq
    sudo rm -rf /app/cloudflare-ddns
    sudo rm /etc/cron.d/cloudflare-ddns
    sudo rm /var/log/cloudflare_ddns.log
    sudo rm /var/log/cloudflare_ddns.log.*
    echo "Done"
else
    echo "Uninstallation is cancelled."
fi
