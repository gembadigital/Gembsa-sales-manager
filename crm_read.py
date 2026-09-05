#!/usr/bin/env python3
"""Sabit, salt-okunur Gemba IQ CRM okuma script'i.

Kullanim: python3 crm_read.py "<kaynak>/search?<query>"
Sadece deals|leads|outreach|companies|contacts|tasks 'search' uclarina GET
yapar. Baska bir HTTP metodu YOKTUR - bu dosyada .post/.patch/.delete
cagrisi bulunmamalidir (bu, exec-approval allowlist'inin bu script'e
guvenmesinin tek nedeni; icerik degisirse hash kontrolu yakalar).
"""
import re
import sys

import requests

BASE_URL = "https://gemba-iq.vercel.app/api/organization/integration"
ALLOWED_PATH = re.compile(
    r"^(deals|leads|outreach|companies|contacts|tasks)/search(\?[A-Za-z0-9=&%,._\-]*)?$"
)


def main():
    if len(sys.argv) != 2:
        print("Kullanim: python3 crm_read.py \"<kaynak>/search?<query>\"", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not ALLOWED_PATH.match(path):
        print(f"REDDEDILDI: '{path}' izin verilen okuma deseniyle eslesmiyor.", file=sys.stderr)
        sys.exit(1)

    with open("gemba-iq-api-key.txt", "r") as f:
        api_key = f.read().strip()

    resp = requests.get(
        f"{BASE_URL}/{path}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    print(resp.text)


if __name__ == "__main__":
    main()
