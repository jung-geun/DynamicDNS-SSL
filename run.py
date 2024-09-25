import sys
from dynamicdns_ssl import DDNS


if __name__ == "__main__":
    API = DDNS()
    config = API.get_config()

    # Check if the IP has changed
    results = API.update_a_list(config["CLOUDFLARE_A"], API.current_ip)

    API.update_ip(API.current_ip)

    # Update CNAME records
    result = API.update_cname_list(config["CLOUDFLARE_CNAME"])

    sys.exit(0)
