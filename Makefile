DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install     Install the required dependencies"
	@echo "  certbot     Install certbot"
	@echo "  uninstall   Uninstall the installed dependencies"
	@echo ""

.PHONY: install
install:
	@scripts/install.sh

.PHONY: certbot
certbot:
	@scripts/certbot.sh

.PHONY: uninstall
uninstall:
	@scripts/uninstall.sh
