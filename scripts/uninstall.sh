#!/bin/bash
@echo "Uninstalling Cloudflare DDNS and Certbot..."
@sudo rm -rf /app/cloudflare-ddns
@sudo rm /etc/cron.d/cloudflare-ddns
@sudo rm /var/log/cloudflare_ddns.log
@sudo rm /var/log/cloudflare_ddns.log.*
@echo "Done"