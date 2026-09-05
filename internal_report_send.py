#!/usr/bin/env python3
"""Dar kapsamli, ic ekip rapor gonderme script'i.

SADECE sabit ic ekip adreslerine gonderir - alici listesi kod icinde
sabittir, hicbir parametreyle degistirilemez. Serbest icerik/adres
alan genel bir mail gonderme araci DEGILDIR - outreach/satis maili
icin KULLANILAMAZ (o hala insan onayi gerektiren ayri bir akistir).

Kullanim: python3 internal_report_send.py "<konu>"
Govde, ayni dizindeki internal_report_content.txt dosyasindan okunur
(agent bu dosyayi 'write' araciyla onceden yazar - boylece bu script'in
komut satiri her zaman sabit/kisa kalir, exec-approval allowlist'i
guvenle eslesebilir).
"""
import json
import sys

import requests

RECIPIENTS = ["a.zehir@gembapartner.com", "e.ozakin@gembapartner.com"]
ALLOWED_SUBJECTS = {
    "Pazartesi Prospecting Özeti",
    "Çarşamba Rakip Prospecting Özeti",
    "Haftalık Değerlendirme Özeti",
}
BASE_URL = "https://gemba-iq.vercel.app/api/organization/integration"
CONTENT_FILE = "internal_report_content.txt"


def main():
    if len(sys.argv) != 2:
        print(f"Kullanim: python3 internal_report_send.py \"<konu>\" ({'|'.join(sorted(ALLOWED_SUBJECTS))})", file=sys.stderr)
        sys.exit(1)

    subject = sys.argv[1]
    if subject not in ALLOWED_SUBJECTS:
        print(f"REDDEDILDI: '{subject}' izin verilen konu basliklari arasinda degil.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            body = f.read().strip()
    except FileNotFoundError:
        print(f"REDDEDILDI: {CONTENT_FILE} bulunamadi - once rapor metnini bu dosyaya yaz.", file=sys.stderr)
        sys.exit(1)

    if not body:
        print("REDDEDILDI: rapor icerigi bos.", file=sys.stderr)
        sys.exit(1)

    with open("gemba-iq-api-key.txt", "r") as f:
        api_key = f.read().strip()

    full_subject = f"[Gemba IQ] {subject}"
    html_body = "<p>" + body.replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"

    payload = {
        "to": RECIPIENTS,
        "subject": full_subject,
        "body": body,
        "html": html_body,
    }
    resp = requests.post(
        f"{BASE_URL}/mail/send",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    print(resp.text)


if __name__ == "__main__":
    main()
