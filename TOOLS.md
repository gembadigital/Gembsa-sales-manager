# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup: camera names and locations, SSH hosts and aliases, preferred TTS voices, speaker/room names, device nicknames, anything environment-specific.

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)

### Gemba IQ CRM API (OpenClaw entegrasyonu)
- Base URL: https://gemba-iq.vercel.app/api/organization/integration
- Auth: her istekte `Authorization: Bearer <key>` header'ı gerekli.
- Key: bu workspace'teki `gemba-iq-api-key.txt` dosyasında saklı — istek anında oku, sadece Authorization header'ında kullan, asla loglama/yazdırma/başka yere kopyalama.
- localhost'ta çalışan bir proxy/servis YOK — her zaman doğrudan yukarıdaki Vercel adresine git, localhost:8080 gibi bir adres uydurma.
- Tam endpoint listesi ve scope tanımları için: gemba-iq reposundaki docs/openclaw-integration.md (companies/contacts/deals/tasks/mail/leads/outreach).
- `mail:send` ile gönderilen HER e-postanın konu başlığı (`subject`) MUTLAKA
  `[Gemba IQ] ` ön ekiyle başlamalı (ör. `[Gemba IQ] Haftalık Fırsat Raporu`,
  `[Gemba IQ] Pazartesi Prospecting Özeti`). Bu, `info@gembapartner.com`
  adresinden giden otomatik raporları elle atılan maillerden ayırt etmek için.
- CRM arama uçlarındaki (`contacts/search`, `leads/search`, `outreach/search`) `query` parametresi güvenilmez, filtrelemiyor (test edildi: farklı sorgu değerleri aynı sonucu döndürüyor). Bu uçlar ASLA isim/içerik bazlı arama için `query` ile çağrılmaz. Bunun yerine: `status` (ve varsa tarih) alanına göre ilgili tüm kayıtlar çekilir, isim/alıcı eşleştirmesi agent tarafından sonuçlar üzerinde manuel yapılır.
- Salt-okuma CRM sorgularında (`deals/search`, `leads/search`, `outreach/search`, `contacts/search`, `companies/search` — hepsi GET) curl çıktısını mümkünse `>` ile dosyaya YÖNLENDİRME, doğrudan stdout'ta bırak (sonucu bir sonraki adımda zaten okuyabilirsin). Bu, bu komutların otomatik onaydan faydalanmasını sağlıyor — dosyaya yönlendirme onay sürecini yavaşlatıyor. Zorunlu olarak dosyaya kaydetmen gerekiyorsa (ör. çok büyük bir sonuç), sadece basit bir dosya adı kullan (`deals.json` gibi — yol/`/` veya `~` içermeyen), çünkü sadece bu kalıp otomatik onaylanabiliyor.
- Birden fazla firma/kişi için ardışık `curl` çağrısı gerekiyorsa (ör. toplu taslak oluşturma), Python sözdizimini (`for x, y in [(...), (...)]:`) bash içinde KULLANMA — bash'te geçersizdir ve tüm komut bloğu çöker. Bunun yerine ya her kayıt için AYRI bir `exec` çağrısı yap (tek `curl` = tek exec çağrısı), ya da bash'e uygun bir döngü kullan. Bir komut bloğunu göndermeden önce saf bash olarak çalışır mı diye kontrol et; emin değilsen tek satırlık, tek amaçlı komutları tercih et.
- `POST /outreach` çağrısı ZORUNLU olarak `recipients` alanı ister —
  `[{"name": "Ad Soyad", "email": "kisi@firma.com"}]` formatında, non-empty
  array. `companyName` gibi var olmayan bir alan İCAT ETME — API bunu kabul
  etmez, `{"error":"'recipients' (non-empty array) is required."}` ile
  reddeder (bu gerçekten yaşandı). Eğer karar verici isim/mail
  bulunamadıysa, `recipients` alanına firma bilgisini UYDURMA — bu durumda
  taslak oluşturma denemesi hiç yapılmaz, firma raporda "karar verici
  bulunamadığı için taslak oluşturulamadı" diye açıkça işaretlenir.
