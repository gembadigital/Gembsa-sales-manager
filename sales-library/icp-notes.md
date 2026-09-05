# ICP Notları — Gemba Partner

*Kaynak: SOUL.md'deki taban ICP kriterleri + `deals.json` (2026-08-31 CRM export'u) üzerinden çıkarılan gerçek kazanılan/kaybedilen fırsat örüntüleri. Bu dosya SOUL.md'deki resmi ICP kriterlerinin YERİNE geçmez, onu somut vaka örüntüleriyle destekler.*

## Taban kriterler (SOUL.md'den, değişmez)

- Çalışan sayısı: 150 ve üzeri
- Yıllık ciro: genel olarak 20 milyon USD ve üzeri
- Sektör: sınırlama yok (üretim/sanayi ağırlıklı ama lojistik, hizmet, depo, perakende dahil)
- Coğrafya: sadece Türkiye
- Üst sınır yok, ama karar vericiye gerçekten ulaşılabilir olmalı

## Gerçekte kazanılan profil (20 Won fırsat, deals.json'dan)

- **Sektör ağırlığı**: Ezici çoğunluk üretim/sanayi (13/20 doğrudan "Manufacturing", +3 "Üretim/Diğer Sektörler" etiketli, hepsi fiilen üretim). Tarım ekipmanları ve otomotiv yan sanayi de kazanılmış örnekler arasında.
- **En çok satılan ürün**: "Proje Danışmanlığı" (12/20) — asıl kazanç kalemi. "Eğitim" (3) ve "Koçluk Çalışması" (2) daha küçük/hızlı satılan giriş ürünleri olarak işlev görüyor.
- **Fırsat büyüklüğü**: 70.000 TL – 4.500.000 TL aralığı, ortalama ~1.25M TL. Eğitim/Koçluk gibi giriş ürünleri 70K–390K bandında, büyük "Proje Danışmanlığı" anlaşmaları 1M–4.5M TL bandında.
- **Man-day**: Kazanılan projelerde 3–96 man-day arası geniş bir yelpaze var — küçük değerlendirme/eğitim işleri (3–14 gün) büyük OPEX projelerine (48–96 gün) kapı aralayan giriş noktaları olabiliyor.
- **Lead source**: CRM'de görülen örneklerden biri "İnternette Araştırma" — inbound/organik ilgi de gerçek bir kazanma kanalı, sadece soğuk outreach değil.

## Gerçekte kaybedilen/askıya alınan örüntüler

Aşağıdaki gerekçeler `deals.json`'daki gerçek "Lost/Kapandı Kaybedildi" kayıtlarının `description` alanlarından alınmıştır (bkz. [[objection-handling]]):

- Ekonomik koşullar nedeniyle iptal ("Mevcut Ekonomik durumdan dolayı firma projeyi iptal etti")
- Bütçe zamanlaması ("2027 Bütçesi için görüşülecek" — kayıp değil, erteleme)
- Hazır olmama ("Firma bu çalışmalar hazır değil")
- Konunun askıya alınması (net gerekçe belirtilmeden "Askıya Alındı")
- Çoğu kayıp kaydında (19/24) hiç gerekçe notu girilmemiş — bu, kaybedilen fırsatlarda çıkış görüşmesi/gerekçe kaydının sistematik olmadığını gösteriyor; ileride "neden kaybettik" verisini iyileştirmek isteniyorsa bu bir süreç boşluğu olarak not edilebilir.

## Bu notların kullanım amacı

Prospecting (Pazartesi/Çarşamba) ve yeniden temas (Salı/Perşembe) görevlerinde:
- Lead Score verirken "Proje Danışmanlığı"na aday, üretim ağırlıklı, 150+ çalışanlı firmaları öncelikli gör — geçmiş kazanma örüntüsüyle örtüşüyor.
- Küçük/orta ölçekli ama ICP'ye giren firmalarda "Eğitim" veya "Koçluk Çalışması" gibi daha düşük bariyerli bir giriş teklifi, doğrudan büyük "Proje Danışmanlığı" teklifinden daha gerçekçi bir ilk adım olabilir.
- Bütçe/zamanlama itirazı (`2027 bütçesi`, `şu an sırası değil` gibi) geldiğinde bunu kesin bir "hayır" değil, geçmişte de görülen bir erteleme örüntüsü olarak değerlendir — [[objection-handling]] dosyasındaki ilgili bölüme bak.

---
*Not: Bu dosyadaki sayılar 2026-08-31 tarihli bir CRM export'undan (`deals.json`, 69 kayıt) türetilmiştir, canlı veri değildir. Güncel/kesin rakam gerektiğinde CRM'den `status`'e göre çekilip client-side filtrelenmelidir (TOOLS.md kuralı).*
