import json
import logging
import logging.handlers
import os
import sys
from typing import Literal, Optional

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger("requests").setLevel(logging.WARNING)
fileHandler = logging.handlers.RotatingFileHandler(
    "/var/log/cloudflare_ddns.log", maxBytes=100000, backupCount=5
)
fileHandler.setFormatter(format)

logger.addHandler(fileHandler)
logger.addHandler(logging.StreamHandler())


class DDNS:
    def __init__(self, config_path="/app/cloudflare-ddns/config/env.json"):
        self.config = self.load_config(config_path)
        current_ip = self.get_ip()
        previous_ip = self.previous_ip()

        logger.info(f"External IP: {current_ip}")
        logger.info(f"Previous IP: {previous_ip}")
        self.current_ip = current_ip
        self.cname_list = self.config["CLOUDFLARE_CNAME"]

    def load_config(self, config_path="/app/cloudflare-ddns/config/env.json"):
        config = {}
        required_keys = [
            "CLOUDFLARE_API_KEY",
            "CLOUDFLARE_DOMAIN",
            "CLOUDFLARE_ZONE_ID",
        ]

        # 1. env.json 파일에서 설정 로드 (있는 경우)
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                config = json.load(file)

        # 2. 환경 변수에서 설정 로드 (파일에 없는 경우에만)
        for key in required_keys:
            if key not in config and key in os.environ:
                config[key] = os.getenv(key)

        # 3. 필수 키가 모두 있는지 확인
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_keys)}"
            )

        return config

    def get_config(self):
        return self.config

    def get_ip(self):
        try:
            response = requests.get("https://ifconfig.me")
            return response.text
        except Exception as e:
            logger.error(f"Error: {e}")
            # print(f"Error: {e}")
            return None

    def previous_ip(self):
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

    def check_ip(self):
        """
        다르면 True, 같으면 False

        Returns:
            bool: 다르면 True, 같으면 False
        """
        if self.get_ip() != self.previous_ip():
            return True
        return False

    def update_ip(self, ip):
        try:
            with open("/tmp/external_ip.txt", "w") as file:
                file.write(ip)
        except Exception as e:
            logger.error(f"Error: {e}")
            # print(f"Error: {e}")
            return None

    def read_record(self, type=Literal["A", "CNAME"], name=None, content=None):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['CLOUDFLARE_API_KEY']}",
            }
            params = {
                "type": type,
                "name": name,
                "content": content,
            }
            response = requests.get(url, headers=headers, params=params)
            records = response.json()["result"]
            return records if records else None
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.warning("recommendation: check the environment variables")
            # print(f"Error: {e}")
            return -1

    def create_record(
        self, type=Literal["A", "CNAME"], name=None, content=None, proxy=True
    ):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['CLOUDFLARE_API_KEY']}",
            }
            data = {
                "type": type,
                "name": name,
                "content": content,
                "ttl": 1,
                "proxied": proxy,
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            success = response.json()["success"]
            return success if success else None
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.warning("recommendation: check the environment variables")
            # print(f"Error: {e}")
            return -1

    def update_record(
        self, record_id, type=Literal["A", "CNAME"], name=None, content=None, proxy=True
    ):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records/{record_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['CLOUDFLARE_API_KEY']}",
            }
            data = {
                "type": type,
                "name": name,
                "content": content,
                "ttl": 1,
                "proxied": proxy,
            }
            response = requests.put(url, headers=headers, data=json.dumps(data))
            success = response.json()["success"]
            return success if success else None
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.warning("recommendation: check the environment variables")
            # print(f"Error: {e}")
            return -1

    def delete_record(self, record_id):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records/{record_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['CLOUDFLARE_API_KEY']}",
            }
            response = requests.delete(url, headers=headers)
            success = response.json()["success"]
            return success if success else None
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.warning("recommendation: check the environment variables")
            # print(f"Error: {e}")
            return -1

    def update_cname_list(self, cname_list, domain):
        try:
            records_list = self.read_record(type="CNAME", content=domain)
            if records_list == -1:
                logger.error("Failed to get DNS records")
                return None
            elif not records_list:
                for cname, proxy in cname_list.items():
                    result = self.create_record(
                        type="CNAME", name=cname, content=domain, proxy=proxy
                    )
                    logger.info(f"{cname} is created")
            else:
                pre_list = {}
                for r in records_list:
                    pre_list[r["name"].split(".")[0]] = [r["proxied"], r["id"]]

                for cname, proxy in cname_list.items():
                    if cname in pre_list.keys():
                        if proxy != pre_list[cname][0]:
                            self.update_record(
                                record_id=r["id"],
                                type="CNAME",
                                name=cname,
                                content=domain,
                                proxy=proxy,
                            )
                            logger.info(f"{cname} is updated")
                        pre_list.pop(cname)
                    else:
                        result = self.create_record(
                            type="CNAME", name=cname, content=domain, proxy=proxy
                        )
                        logger.info(f"{cname} is created")
                for p in pre_list:
                    records = self.read_record(type="CNAME", name=p + "." + domain)
                    record_id = records[0]["id"]
                    result = self.delete_record(record_id)
                    logger.info(f"{p} is deleted")
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.warning("recommendation: check the environment variables")
            # print(f"Error: {e}")
            return -1


if __name__ == "__main__":
    API = DDNS()
    config = API.get_config()
    flag = API.check_ip()

    if flag:
        logger.info("IP has changed")

        a_records = API.read_record(type="A", name=config["CLOUDFLARE_DOMAIN"])

        if a_records == -1:
            logger.error("Failed to get DNS records")
            sys.exit(0)
        elif not a_records:
            logger.info("No records found")
            result = API.create_record(
                type="A", name=config["CLOUDFLARE_DOMAIN"], content=API.current_ip
            )
            API.update_ip(API.current_ip)
        else:
            ip_list = [API.get_ip(), API.previous_ip()]

            for a_record in a_records:
                if a_record["content"] in ip_list:
                    logger.info(
                        f"{a_record['type']} type | {a_record['name']} | {a_record['content']}"
                    )

                    record_id = a_record["id"]

                    result = API.update_record(
                        record_id=record_id,
                        type="A",
                        name=config["CLOUDFLARE_DOMAIN"],
                        content=API.current_ip,
                    )

            API.update_ip(API.current_ip)

        if not result:
            logger.error("Failed to update DNS A record")
            #     # print("Failed to update DNS record")
            sys.exit(0)

    else:
        logger.info("IP has not changed")

    # Update CNAME records
    API.update_cname_list(config["CLOUDFLARE_CNAME"], config["CLOUDFLARE_DOMAIN"])

    sys.exit(0)
