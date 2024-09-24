# Cloudflare DDNS Project

This project aims to implement a Dynamic DNS (DDNS) solution using Cloudflare's API. 

[![Quality Gate Status](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=alert_status&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)
[![Security Hotspots](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=security_hotspots&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)
[![Bugs](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=bugs&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)

## Overview
Dynamic DNS allows you to associate a domain name with a changing IP address, making it easier to access your network resources remotely. Cloudflare's API provides the necessary tools to automate this process.

## Prerequisites
Before getting started, make sure you have the following:

- A Cloudflare account
- A registered domain name
- API credentials from Cloudflare

## Installation
To install and set up the project, follow these steps:

1. Clone the repository: `git clone https://github.com/jung-geun/cloudflare-ddns.git`
2. Deploy the project to a server or cloud platform: 
    - You can deploy the project to a server or cloud platform of your choice. 
    - Make sure to install the necessary dependencies by running 'make install'
3. Configure the project:
    - Create a configuration file named `config.json` in the initial 
    'make configure' will create a configuration file with default settings.
    - Add your Cloudflare API credentials and domain information to the configuration file.


## Usage
Once the project is up and running, it will periodically check for IP address changes and update the DNS records accordingly. You can customize the update frequency and other settings in the configuration file.

## Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
## 기여하기
기여는 환영합니다! 제안이나 개선 사항이 있으시면 이슈를 열거나 풀 리퀘스트를 제출해 주세요.

## 라이선스
이 프로젝트는 MIT 라이선스로 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.