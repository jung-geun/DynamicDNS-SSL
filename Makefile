IMAGE_NAME = "cloudflare-ddns"

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
	@echo "Installing cloudflare-ddns to '/app/cloudflare-ddns'"
	@mkdir -p /app/cloudflare-ddns
	@cp -r ./* /app/cloudflare-ddns
	@if [ ! -f /app/cloudflare-ddns/config/env.json ]; then \
		echo "Creating default env.json"; \
		mkdir -p /app/cloudflare-ddns/config; \
    	cp /app/cloudflare-ddns/init/default_env.json /app/cloudflare-ddns/config/env.json; \
		echo "Please edit /app/cloudflare-ddns/config/env.json"; \
	fi
	@cp /app/cloudflare-ddns/cron/cronjob /etc/cron.d/cloudflare-ddns
	@touch /var/log/cloudflare_ddns.log
	@chmod +x /app/cloudflare-ddns/run_script.sh
	@chmod +x /app/cloudflare-ddns/start.sh
	
	@echo "Enter 'make configure' to configure the Cloudflare API key, domain and ZONE ID"

	@echo "Done"

.PHONY: configure
configure:
	@echo "Please edit /app/cloudflare-ddns/config/env.json"
	@vi /app/cloudflare-ddns/config/env.json
	@echo "Done"