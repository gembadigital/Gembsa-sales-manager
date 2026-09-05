# Lead Skorlama Modeli

*Kaynak: Claude'un `small-business:lead-triage` ve `small-business:call-list` skill'lerinden uyarlanmıştır (2026-09-03, sohbete yapıştırıldı). Perşembe "Yeniden Temas" görevine ve genel lead önceliklendirmesine referans — Atakan'ın "hangi aday gerçekten sıcak" sorusuna, güvenilir olmayan bir GitHub scraper'ı yerine, mevcut CRM verisiyle çalışan bir puanlama disipliniyle cevap verir.*

## Dört Boyutlu Skorlama

Her lead/aday için şu boyutlarda değerlendirme yap:

- **Engagement (Etkileşim)** — son 30 gün içindeki e-posta yanıtları, açılmalar, site ziyaretleri (`outreach/search` geçmişinden). 30 günden eski sinyaller "soğuk" say, bunu açıkça belirt.
- **Firma Uyumu (ICP Fit)** — sektör ve büyüklük, [[icp-notes]]'teki ICP tanımına göre. ICP dışı bir sektörse (ör. banka, perakende) düşük puanla ya da hariç tut — **Aslı Arslan/Garanti BBVA vakasında olduğu gibi**, CRM'de "Warm" etiketli olması ICP uyumu garantilemez, ayrıca kontrol et.
- **Aciliyet** — lead'in yaşı, aşamada kaldığı süre; son 24 saat içinde zaten temas kurulmuşsa puanı düşür (bugün tekrar aranmasın).

## Liste Boyutu

Kaç lead bulunduğuna göre ayarla:

- 10 ve altı → hepsini göster
- 11-30 → en üstteki 5'i göster
- 30+ → en üstteki 8'i göster

## Her Lead İçin Çağrı Kartı Formatı

```
{Sıra}. {Kişi Adı} — {Firma}
Fırsat: {tutar varsa} | Aşama: {aşama} | Son temas: {X gün önce}
Sinyal: {en son aktivite}

KONUŞMA NOKTALARI
- {CRM/outreach geçmişinden bir nokta}
- {CRM/outreach geçmişinden bir nokta}
- {sorulacak açık soru}

BU GÖRÜŞMENİN HEDEFİ: {tek cümle — bir sonraki aşamaya geçir / yeniden temas kur / kapat}
```

## Onay Sınırları — değişmez kurallar

- Asla otomatik mail gönderme — sadece taslak, Atakan onaylar/gönderir (mevcut kuralımızla birebir aynı).
- Asla CRM aşamasını/durumunu otomatik değiştirme — Atakan açıkça isterse.
- "Customer" ya da kazanılmış/kapanmış kayıtları lead listesine dahil etme.
- Sıfır lead eşleşirse uydurma — neden sıfır olduğunu açıkça "soğuk, cold outreach gibi yaklaş" diye işaretle — sıcakmış gibi sunma.

## Uygulama notu

Bu model [[crm_read]] script'inin `deals/search`, `leads/search`, `outreach/search` uçlarıyla beslenmeli — ek bir script ya da dış veri kaynağı gerekmiyor. Skorlama sonuçları `outcome-log.jsonl`'daki geçmiş sonuçlarla da çapraz kontrol edilebilir (hangi skor aralığındaki lead'ler gerçekten dönüşüyor) — zamanla model kalibre edilebilir.
