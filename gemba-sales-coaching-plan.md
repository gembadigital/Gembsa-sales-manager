# Gemba Sales Manager — Satış Kütüphanesi & Koçluk Sistemi (Faz Planı)

*Hazırlanma tarihi: 2026-09-02 — Cowork oturumunda tartışıldı, uygulama VPS terminalindeki Claude Code oturumuna devredilecek.*

## Kapsam (onaylanan üç hedef)

1. **Outreach taslak kalitesi** — Agent'ın ürettiği mesajların itiraz yönetimi, başarı hikayeleri ve geçmiş sonuçlardan öğrenerek iyileşmesi.
2. **Deal bazlı tavsiye** — Agent'ın "şu lead'e şöyle yaklaş, şimdi takip et" gibi Atakan'ın karar almasına yardımcı öneriler sunması.
3. **Proaktif fırsat taraması** — Gemba IQ CRM'i bir satış koçu gibi tarayıp açıkta bekleyen/temassız kalmış fırsatları değerlendirmesi, temas önerisinde bulunması, CRM verisini aksiyona dönüştürmesi.

## Yaklaşım: ML değil, yapılandırılmış kütüphane + geri besleme

Gerçek model eğitimi (fine-tuning) reddedildi — maliyetli ve gereksiz. Bunun yerine:

- **Statik kütüphane**: objection-handling, ICP notları, başarı hikayeleri (Pilsan/Sunman gibi) — ayrı referans dosyaları olarak workspace'e eklenip SOUL.md'den bağlanacak.
- **Sonuç geri beslemesi**: hangi taslağın işe yaradığı/yaramadığı kayıt altına alınıp gelecekteki taslaklara girdi olacak.

Bu, sıfır ek API/altyapı maliyetiyle agent'ı zamanla "daha tecrübeli" hale getirir — bütçe kısıtına (ücretli API/MCP yok) tamamen uygun.

## Kaynak materyal (onaylanan üçü de)

- Sıfırdan, tanınmış satış metodolojilerinden (itiraz yönetimi kalıpları, değer önerisi çerçeveleri) ICP'ye göre uyarlanmış içerik
- Geçmiş CRM verisi — kazanılan/kaybedilen deal notları, gerçek vakalar (Pilsan/Sunman gibi)
- Atakan'ın elindeki mevcut satış dokümanları/scriptleri (varsa — iletilmesi gerekiyor)

## Faz 1 — Kütüphane + SOUL.md entegrasyonu (düşük risk)

- Yeni referans dosyaları: `sales-library/objection-handling.md`, `sales-library/success-stories.md`, `sales-library/icp-notes.md` (workspace-gemba-sales altında)
- SOUL.md'ye bu dosyalara referans veren kısa bir bölüm eklenmesi
- Kod/altyapı değişikliği gerektirmiyor — sadece içerik + prompt güncellemesi
- **Bilinen risk**: geçmiş deal verisini toplarken CRM'in kırık `query` param bug'ına takılmamak için "status'a göre çek, client-side filtrele" kuralına uyulmalı (zaten mevcut kural)

## Faz 2 — Outreach kalite döngüsü (orta risk)

- Draft-sonuç eşleştirmesi için iki seçenek:
  - **A (hızlı başlangıç, şema değişmeden)**: workspace içinde ayrı bir `outcome-log.jsonl` — Atakan Telegram'dan "bu taslak işe yaradı/yaramadı" diye bildirdikçe agent kaydediyor
  - **B (kalıcı çözüm)**: Gemba IQ CRM şemasına bir `outcome`/`result` alanı eklenmesi — bu, zaten dev-team backlog'unda bekleyen `query` param ve `batchId` sorunlarıyla aynı kategoride, ayrı bir konu olarak Gemba IQ tarafına iletilmeli
- Öneri: Faz 2'ye A ile başla, B'yi dev-team backlog'una ekle

## Faz 3 — Proaktif fırsat/koçluk taraması (en yüksek risk)

- Yeni bir görev (örn. haftalık, mevcut "gemba-cuma-degerlendirme" görevine entegre ya da ayrı bir "gemba-pipeline-coach" cron'u): açık deal'leri tarar, X gündür temassız kalanları/"Yeni" kolonunda bekleyenleri flag'ler, Telegram'a öneri raporu gönderir
- **Kritik kısıt (2026-09-01 bulgusu ile aynı)**: salt-okunur CRM taramaları bile exec-approval'a takılıyor; otomatik onay teknik olarak imkansız (OpenClaw mimarisinde kanıtlanmış). Kimse Telegram'da değilken çalışırsa aynı 30 dakikalık timeout riski var.
- Bu yüzden bu görev ya (a) Atakan'ın gerçekten Telegram'da olduğu bir saate planlanmalı, (b) "toplu-onay" akışına uygun tasarlanmalı, ya da (c) uzun vadede ayrı bir MCP-plugin projesiyle (daha önce tespit edilen tek gerçek çözüm) exec-approval'ı tamamen bypass edecek şekilde kurulmalı

## Açık teknik sorular — VPS terminalinde kontrol edilmeli

- `outreach_drafts` / `deals` tablosunda kullanılabilir bir outcome/sonuç alanı var mı?
- Faz 3'teki tarama görevi gerçekten salt-okunur mu kalabiliyor, yoksa mevcut mimaride her CRM sorgusu exec/bash üzerinden mi geçiyor (2026-09-01 bulgusuna göre öyle görünüyor)?

## Önerilen sıralama

1. **Faz 1** — hemen başlanabilir, düşük risk, kod değişikliği yok
2. **Faz 2 (seçenek A)** — Faz 1 oturduktan sonra, orta risk
3. **Faz 3** — en son, exec-approval kısıtı netleşene/MCP-plugin projesi konuşulana kadar dikkatli ilerlenmeli

---
*Bu belge, VPS terminalindeki Claude Code oturumuna aktarılıp adım adım uygulanmak üzere hazırlanmıştır. Uygulama sırasında ortaya çıkacak her adım, projenin bugüne kadarki alışkanlığına uygun şekilde küçük adımlarla test edilip Telegram üzerinden doğrulanmalıdır.*
