import logging.handlers
import os
import sys
import requests
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
request_log = logging.getLogger("requests").setLevel(logging.WARNING)
fileHandler = logging.handlers.RotatingFileHandler(
    "/var/log/cloudflare_ddns.log", maxBytes=100000, backupCount=5
)
fileHandler.setFormatter(format)

logger.addHandler(fileHandler)
logger.addHandler(logging.StreamHandler())



def load_config():
    config = {}
    required_keys = ["CLOUDFLARE_API_KEY", "CLOUDFLARE_DOMAIN", "CLOUDFLARE_ZONE_ID"]

    # 1. env.json 파일에서 설정 로드 (있는 경우)
    json_file = "/app/cloudflare-ddns/config/env.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            config = json.load(file)
            

    # 2. 환경 변수에서 설정 로드 (파일에 없는 경우에만)
    for key in required_keys:
        if key not in config and key in os.environ:
            config[key] = os.getenv(key)

    # 3. 필수 키가 모두 있는지 확인
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")

    return config


def get_ip():
    try:
        response = requests.get("https://ifconfig.me")
        return response.text
    except Exception as e:
        logger.error(f"Error: {e}")
        # print(f"Error: {e}")
        return None


def previous_ip():
    try:
        if os.path.exists("/tmp/external_ip.txt"):
            with open("/tmp/external_ip.txt", "r") as file:
                return file.read()
        else:
            os.mknod("/tmp/external_ip.txt")
    except Exception as e:
        logger.error(f"Error: {e}")
        # print(f"Error: {e}")
        return None


def update_ip(ip):
    try:
        with open("/tmp/external_ip.txt", "w") as file:
            file.write(ip)
    except Exception as e:
        logger.error(f"Error: {e}")
        # print(f"Error: {e}")
        return None


def get_record(zone_id, domain_name, api_key):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        params = {
            "type": "A",
            "name": domain_name,
        }
        response = requests.get(url, headers=headers, params=params)
        records = response.json()["result"]
        return records if records else None
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.warning("recommendation: check the environment variables")
        # print(f"Error: {e}")
        return None


def update_dns_record(zone_id, record_id, record_name, ip_address, api_key):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        data = {
            "type": "A",
            "name": record_name,
            "content": ip_address,
            "ttl": 1,
            "proxied": True,
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        success = response.json()["success"]
        return success if success else None
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.warning("recommendation: check the environment variables")
        # print(f"Error: {e}")
        return None


if __name__ == "__main__":
    config = load_config()

    external_ip = get_ip()
    logger.info(f"External IP: {external_ip}")
    # print(f"External IP: {external_ip}")
    previous_ip_ = previous_ip()
    logger.info(f"Previous IP: {previous_ip_}")
    # print(f"Previous IP: {previous_ip_}")

    if external_ip != previous_ip_:
        logger.info("IP has changed")
        # print("IP has changed")

        records = get_record(
            config["CLOUDFLARE_ZONE_ID"],
            config["CLOUDFLARE_DOMAIN"],
            config["CLOUDFLARE_API_KEY"],
        )
        if not records:
            logger.warning("No records found")
            # print("No records found")
            sys.exit(0)

        record_id = records[0]["id"]

        result = update_dns_record(
            config["CLOUDFLARE_ZONE_ID"],
            record_id,
            config["CLOUDFLARE_DOMAIN"],
            external_ip,
            config["CLOUDFLARE_API_KEY"],
        )
        if not result:
            logger.error("Failed to update DNS record")
            # print("Failed to update DNS record")
            sys.exit(0)

        update_ip(external_ip)
        logger.info("IP has been updated")
        # print("IP has been updated")
    else:
        logger.info("IP has not changed")
        # print("IP has not changed")
        sys.exit(0)
