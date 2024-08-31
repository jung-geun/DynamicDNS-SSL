FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    cron \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/cloudflare-ddns/
WORKDIR /app/cloudflare-ddns
RUN mkdir -p /app/cloudflare-ddns/config

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN cp /app/cloudflare-ddns/cron/cronjob /etc/cron.d/cloudflare-ddns

RUN touch /var/log/cron.log
RUN chmod +x /app/cloudflare-ddns/start.sh
RUN chmod +x /app/cloudflare-ddns/run_script.sh

VOLUME [ "/app/cloudflare-ddns/config" ]

ENTRYPOINT [ "bash", "-c" ]

CMD [ "/app/cloudflare-ddns/start.sh && cron -f" ]