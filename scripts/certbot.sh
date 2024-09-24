#!/bin/bash

# Certbot 및 Cloudflare API 도구 설치

# 필요한 변수 설정
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

CONFIG_FILE="$DIR/../config/env.json"
DOMAIN=$(jq -r '.CLOUDFLARE_DOMAIN' $CONFIG_FILE)
CERTBOT_EMAIL=$(jq -r '.EMAIL' $CONFIG_FILE)
CLOUDFLARE_API_TOKEN=$(jq -r '.CLOUDFLARE_API_KEY' $CONFIG_FILE)

# Cloudflare API 자격 증명 파일 생성
CLOUDFLARE_CREDENTIALS_FILE="/etc/letsencrypt/cloudflare.ini"
sudo mkdir -p /etc/letsencrypt
sudo bash -c "echo 'dns_cloudflare_api_token = ${CLOUDFLARE_API_TOKEN}' > ${CLOUDFLARE_CREDENTIALS_FILE}"
sudo chmod 600 ${CLOUDFLARE_CREDENTIALS_FILE}

# Certbot을 사용하여 인증서 발급 및 갱신
sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials ${CLOUDFLARE_CREDENTIALS_FILE} \
  --email ${CERTBOT_EMAIL} \
  --agree-tos \
  --no-eff-email \
  -d "*.${DOMAIN}" \
  -d "${DOMAIN}"

# 크론탭을 사용하여 자동 갱신 설정 (매일 0시, 12시 실행)
echo "0 0,12 * * * /usr/bin/certbot renew --dns-cloudflare --dns-cloudflare-credentials ${CLOUDFLARE_CREDENTIALS_FILE} --quiet" > $DIR/../cron/cronjob-certbot
sudo cp $DIR/../cron/cronjob-certbot /etc/cron.d/certbot-renew

echo "Certbot and Cloudflare API tools installation completed."
