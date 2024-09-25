# DynamicDNS-SSL

**DynamicDNS-SSL** is a script that automatically performs dynamic DNS updates (DDNS) through Cloudflare and automatically renews SSL certificates using Certbot. This project helps domain owners manage their DNS and SSL certificates automatically without the need for manual updates whenever the IP address changes.

This project is useful for individuals using dynamic IPs or small-scale server operators.

[![Quality Gate Status](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=alert_status&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)
[![Security Hotspots](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=security_hotspots&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)
[![Bugs](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=bugs&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)

## Key Features

- **Automatic DNS Updates**: Automatically updates DNS records using the Cloudflare API whenever the IP address changes.
- **Automatic SSL Certificate Renewal**: Automatically issues and renews SSL certificates using Certbot.
- **Configuration File Usage**: Easily change settings through a JSON configuration file.

## Requirements

Before getting started, ensure you have the following:

- Cloudflare account
- Registered domain name
- Cloudflare API credentials

## Installation

### 1. **Clone the Project**

```bash
git clone https://github.com/jung-geun/cloudflare-ddns.git

<!-- or -->

git clone https://git.pieroot.xyz/jung-geun/cloudflare-ddns.git

cd cloudflare-ddns
```

### 2. Install Required Packages

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-dns-cloudflare jq

<!-- or -->

make install # You can use the Makefile to install packages.
```

### 3. Create Configuration File

```bash
vi /app/cloudflare-ddns/config/env.json
```

Write the configuration file as follows:

```json
{
    "CLOUDFLARE_API_KEY": "your_cloudflare_api_key",
    "CLOUDFLARE_ZONE_ID": "your_cloudflare_zone_id",
    "CLOUDFLARE_DOMAIN": "example.com",
    "EMAIL": "your_email@example.com",
    "CLOUDFLARE_A": {
        "@": true
    },
    "CLOUDFLARE_CNAME": {
        "@": {
            "www": true
        }
    },
    "CLOUDFLARE_MX": {}
}
```

## Contribution

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.
