IMAGE_NAME = "cloudflare-ddns"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

default: build

.PHONY: build
build: stop
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	docker run --rm --privileged=true -d -v /opt/cloudflare-ddns/config:/app/cloudflare-ddns/config $(IMAGE_NAME)

.PHONY: stop
stop:
	@container_id=$$(docker ps -q -f ancestor=$(IMAGE_NAME)); \
	if [ -n "$$container_id" ]; then \
		echo "Stopping container $$container_id"; \
		docker stop $$container_id; \
	else \
		echo "No running container found for image $(IMAGE_NAME)"; \
	fi

.PHONY: install
install:
	@echo "Installing cloudflare-ddns"
	@scripts/install.sh

.PHONY: certbot
certbot:
	@echo "Installing certbot"
	@scripts/certbot.sh

.PHONY: clean
clean:
	@rm -rf /app/cloudflare-ddns
	@rm -rf /app/certbot
	@rm /etc/cron.d/cloudflare-ddns
	@rm /var/log/cloudflare_ddns.log
	@rm /var/log/cloudflare_ddns.log.*
	@echo "Done"