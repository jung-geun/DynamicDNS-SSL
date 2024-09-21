FROM python:3.9-slim

RUN mkdir -p /app/cloudflare-ddns/
WORKDIR /app/cloudflare-ddns
RUN mkdir -p /app/cloudflare-ddns/config

COPY requirements.txt /app/cloudflare-ddns/

COPY ./etc /app/cloudflare-ddns/
COPY ./src /app/cloudflare-ddns/
COPY ./*.sh /app/cloudflare-ddns/

# Install required packages
RUN apt-get update && apt-get --no-install-recommends install -y \
    cron \
    libaugeas0 \
    make \
    python3.11 python3.11-dev python3.11-pip python3.11-venv \
    && rm -rf /var/lib/apt/lists/* \
    cp /app/cloudflare-ddns/cron/cronjob-ddns /etc/cron.d/cloudflare-ddns \
    pip install --no-cache-dir -r requirements.txt \
    touch /var/log/cron.log \
    chmod +x /app/cloudflare-ddns/start.sh \
    chmod +x /app/cloudflare-ddns/run_script.sh

VOLUME [ "/app/cloudflare-ddns/config" ]

ENTRYPOINT [ "bash", "-c" ]

CMD [ "/app/cloudflare-ddns/start.sh && cron -f" ]