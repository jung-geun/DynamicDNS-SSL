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
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d w%H:%M:%S"
)
logging.getLogger("requests").setLevel(logging.WARNING)
fileHandler = logging.handlers.RotatingFileHandler(
    "/var/log/cloudflare_ddns.log", maxBytes=100000, backupCount=5
)
fileHandler.setFormatter(format)

logger.addHandler(fileHandler)
logger.addHandler(logging.StreamHandler())

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/env.json")


class DDNS:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config = self.load_config(config_path)
        current_ip = self.get_ip()
        previous_ip = self.previous_ip()

        logger.info(f"External IP: {current_ip}")
        logger.info(f"Previous IP: {previous_ip}")
        self.current_ip = current_ip
        self.cname_list = self.config["CLOUDFLARE_CNAME"]

        self.HEADERS = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['CLOUDFLARE_API_KEY']}",
        }

    def load_config(self, config_path=DEFAULT_CONFIG_PATH):
        f"""
        환경 변수와 env.json 파일에서 설정을 로드합니다.

        Args:
            config_path (str): 설정 파일 경로. Defaults to {DEFAULT_CONFIG_PATH}.

        Raises:
            ValueError: 필수 설정이 없는 경우

        Returns:
            _type_: _description_
        """
        config = {}
        required_keys = [
            "CLOUDFLARE_API_KEY",
            "CLOUDFLARE_DOMAIN",
            "CLOUDFLARE_ZONE_ID",
            "CLOUDFLARE_A",
            "CLOUDFLARE_CNAME",
            "CLOUDFLARE_MX",
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
                f"Missing required configuration: {', '.join(missing_keys)}",
                "Please set the environment variables or create a config file.",
                required_keys,
            )

        self.domain = config["CLOUDFLARE_DOMAIN"]

        return config

    def get_config(self):
        """
        설정을 반환합니다.

        Returns:
            dict: 설정
        """
        return self.config

    def get_ip(self):
        try:
            response = requests.get("https://ifconfig.me")
            return response.text
        except Exception as e:
            logger.error(f"Error: {e}")
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
            logger.info("IP is updated")
        except Exception as e:
            logger.error(f"UPDATE IP Error: {e}")
            return None

    def read_record(self, type=Literal["A", "CNAME"], name=None, content=None):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records"
            params = {
                "type": type,
                "name": name,
                "content": content,
            }
            response = requests.get(url, headers=self.HEADERS, params=params).json()
            records = response["result"]
            if response["success"] is False:
                raise requests.exceptions.RequestException(
                    f"Failed to get DNS records name : {content} | type : {type}"
                )
            return records if records else None
        except Exception as e:
            logger.error(f"READ RECORD Error: {e}")
            sys.exit(1)

    def create_record(
        self, type=Literal["A", "CNAME"], name=None, content=None, proxy=True
    ):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records"
            data = {
                "type": type,
                "name": name,
                "content": content,
                "ttl": 1,
                "proxied": proxy,
            }
            response = requests.post(
                url, headers=self.HEADERS, data=json.dumps(data)
            ).json()
            success = response["success"]
            if not success:
                raise requests.exceptions.RequestException(f"Failed to create {name}")
            return success if success else None
        except Exception as e:
            logger.error(f"CREATE RECORD Error: {e}")
            sys.exit(2)

    def update_record(
        self, record_id, type=Literal["A", "CNAME"], name=None, content=None, proxy=True
    ):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records/{record_id}"
            data = {
                "type": type,
                "name": name,
                "content": content,
                "ttl": 1,
                "proxied": proxy,
            }
            response = requests.put(
                url, headers=self.HEADERS, data=json.dumps(data)
            ).json()
            success = response["success"]
            if not success:
                raise requests.exceptions.RequestException(f"Failed to update {name}")
            return success if success else None
        except Exception as e:
            logger.error(f"UPDATE RECORD Error: {e}")
            sys.exit(3)

    def delete_record(self, record_id):
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{self.config['CLOUDFLARE_ZONE_ID']}/dns_records/{record_id}"
            response = requests.delete(url, headers=self.HEADERS).json()
            success = response["success"]
            if not success:
                raise requests.exceptions.RequestException(
                    f"Failed to delete {record_id}"
                )
            return success if success else None
        except Exception as e:
            logger.error(f"DELETE RECORD Error: {e}")
            sys.exit(4)

    def update_a_list(self, a_list, ips):
        try:
            records_list = self.read_record(type="A", content=ips)
            if not records_list:
                for a, proxy in a_list.items():
                    self.create_record(type="A", name=a, content=ips, proxy=proxy)
                    logger.info(f"{a} is created")
            else:
                pre_list = {}
                for r in records_list:
                    pre_list[r["name"]] = [r["proxied"], r["id"]]
                for a, proxy in a_list.items():
                    a = (
                        a + "." + self.config["CLOUDFLARE_DOMAIN"]
                        if a != "@"
                        else self.config["CLOUDFLARE_DOMAIN"]
                    )
                    if a in pre_list.keys():
                        if proxy != pre_list[a][0]:
                            self.update_record(
                                record_id=pre_list[a][1],
                                type="A",
                                name=a,
                                content=ips,
                                proxy=proxy,
                            )
                            logger.info(f"{a} is updated")
                        pre_list.pop(a)
                    else:
                        self.create_record(type="A", name=a, content=ips, proxy=proxy)
                        logger.info(f"{a} is created")

                for p in pre_list:
                    records = self.read_record(type="A", name=p)
                    record_id = records[0]["id"]
                    self.delete_record(record_id)
                    logger.info(f"{p} is deleted")

            logger.info("A records are updated")
            return True

        except Exception as e:
            logger.error(f"A RECORDS UPDATE Error: {e}")
            sys.exit(5)

    def update_cname_list(self, cname_list):
        try:
            for a_record in cname_list.keys():
                domain = (
                    a_record + "." + self.domain if a_record != "@" else self.domain
                )

                records_list = self.read_record(type="CNAME", content=domain)
                tmp_cname_list = cname_list[a_record]

                if not records_list:
                    for cname, proxy in tmp_cname_list.items():
                        self.create_record(
                            type="CNAME", name=cname, content=domain, proxy=proxy
                        )
                        logger.info(f"{cname} is created")
                else:
                    pre_list = {}
                    for record in records_list:
                        pre_list[record["name"].split(".")[0]] = [
                            record["proxied"],
                            record["id"],
                        ]

                    for cname, proxy in tmp_cname_list.items():
                        if cname in pre_list.keys():
                            if proxy != pre_list[cname][0]:
                                self.update_record(
                                    record_id=pre_list[cname][1],
                                    type="CNAME",
                                    name=cname,
                                    content=domain,
                                    proxy=proxy,
                                )
                                logger.info(f"{cname} is updated")
                            pre_list.pop(cname)

                        else:
                            self.create_record(
                                type="CNAME", name=cname, content=domain, proxy=proxy
                            )
                            logger.info(f"{cname} is created")

                    for p in pre_list:
                        record = self.read_record(
                            type="CNAME", name=p + "." + self.domain
                        )
                        record_id = record[0]["id"]
                        self.delete_record(record_id)
                        logger.info(f"{p} is deleted")

            logger.info("CNAME records are updated")
            return True
        except Exception as e:
            logger.error(f"CNAME RECORDS UPDATE Error: {e}")
            sys.exit(5)


if __name__ == "__main__":
    API = DDNS()
    config = API.get_config()

    # Check if the IP has changed
    results = API.update_a_list(config["CLOUDFLARE_A"], API.current_ip)

    if not results:
        logger.error("Failed to update DNS A records")
        sys.exit(1)
    else:
        API.update_ip(API.current_ip)

    # Update CNAME records
    result = API.update_cname_list(config["CLOUDFLARE_CNAME"])
    if not result:
        logger.error("Failed to update CNAME records")
        sys.exit(1)

    sys.exit(0)
