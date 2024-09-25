# DynamicDNS-SSL

**DynamicDNS-SSL**는 Cloudflare를 통해 동적 DNS 업데이트(DDNS)를 자동으로 수행하고, Certbot을 이용해 SSL 인증서를 자동으로 갱신하는 스크립트입니다. 이 프로젝트는 도메인 소유자가 IP 주소가 변경될 때마다 수동으로 업데이트할 필요 없이, 자동으로 DNS와 SSL 인증서를 관리할 수 있도록 도와줍니다.

동적 IP를 사용하는 개인 사용자나 작은 규모의 서버 운영자들에게 유용한 프로젝트입니다.

[![Quality Gate Status](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=alert_status&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)
[![Security Hotspots](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=security_hotspots&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)
[![Bugs](https://sonar.pieroot.xyz/api/project_badges/measure?project=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4&metric=bugs&token=sqb_706e3b82fdb379ee29accac27f1bd19726dcb31c)](https://sonar.pieroot.xyz/dashboard?id=jung-geun_cloudflare-ddns_AZIjf9NeRMPvGKjJzls4)

## 주요 기능

- **자동 DNS 업데이트**: Cloudflare API를 사용하여 IP 주소가 변경될 때마다 자동으로 DNS 레코드를 업데이트합니다.
- **SSL 인증서 자동 갱신**: Certbot을 사용하여 SSL 인증서를 자동으로 발급 및 갱신합니다.
- **환경 설정 파일 사용**: JSON 형식의 설정 파일을 통해 쉽게 설정을 변경할 수 있습니다.

## 요구 사항

시작하기 전에 다음 사항을 준비해야 합니다:

- Cloudflare 계정
- 등록된 도메인 이름
- Cloudflare API 자격 증명

## 설치

### 1. **프로젝트 클론**

```bash
git clone https://github.com/jung-geun/cloudflare-ddns.git

<!-- or -->

git clone https://git.pieroot.xyz/jung-geun/cloudflare-ddns.git


cd cloudflare-ddns
```

### 2. **필요한 패키지 설치**

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-dns-cloudflare jq

<!-- or -->

make install # makefile을 이용해 패키지를 설치할 수 있습니다.
```

### 3. **환경 설정 파일 생성**

```bash
vi /app/cloudflare-ddns/config/env.json
```

아래와 같이 환경 설정 파일을 작성합니다:

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

## 기여하기

기여는 환영합니다! 제안이나 개선 사항이 있으시면 이슈를 열거나 풀 리퀘스트를 제출해 주세요.

## 라이선스

이 프로젝트는 MIT 라이선스로 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.
