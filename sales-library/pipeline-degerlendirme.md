# Pipeline Değerlendirme Metodolojisi

*Kaynak: Claude'un `sales:pipeline-review` skill'inden uyarlanmıştır (2026-09-03, sohbete yapıştırıldı). Cuma "Haftalık Değerlendirme" görevine yapılandırılmış, ölçülebilir bir çerçeve kazandırmak için — **mevcut serbest metin analizin YERİNE değil, onu destekleyen bir puanlama/önceliklendirme sistemi olarak** kullanılmalıdır.*

*Kopyalama notu: Kaynak metinde bir yerde bozulma/eksiklik oldu — `[YAPIŞTIRMA HATASI: ...]` ile işaretlendi, uydurulmadı.*

## Pipeline Sağlık Skoru

Her Cuma değerlendirmesinde, mümkünse dört boyutta bir sağlık skoru (0-100) hesaplanmalı:

| Boyut | Ağırlık | Neye bakılır |
|---|---|---|
| Aşama İlerlemesi | 25 puan | Kaç deal 30+ gündür aynı aşamada takılı |
| Aktivite Güncelliği | 25 puan | Kaç deal 14+ gündür temassız |
| Kapanış Tarihi Doğruluğu | 25 puan | Kaç deal'in kapanış tarihi geçmişte kalmış |
| Kontak Kapsamı | 25 puan | Kaç deal tek kişiyle (single-threaded) yürüyor — o kişi ayrılırsa/ilgisini kaybederse deal ölür |

## Deal Önceliklendirme Matrisi

Deal'leri üç kovaya ayır:

- **Bu hafta odaklan** — kapanışa yakın, yüksek değer, aktif
- **Sıcak tut** — bu ay kapanacak
- **[YAPIŞTIRMA HATASI: üçüncü kova tanımı kaynak metinde eksik geldi — muhtemelen "izle"/"düşük öncelik" gibi bir kova, ama net değil. Uydurulmadı.]**

Öncelik sıralaması için ağırlıklandırma (varsayılan, Atakan farklı isterse değişebilir):

| Faktör | Ağırlık | Mantık |
|---|---|---|
| Kapanış tarihi | %30 | Yakın kapanan öncelikli |
| Deal büyüklüğü | %25 | Büyük deal daha çok odak alır |
| Aşama | %20 | Geç aşama daha çok odak alır |
| Aktivite | %15 | Aktif deal'ler önceliklenir |
| Risk | %10 | Düşük riskli olan güvenli bahis |

## Risk Bayrakları — her Cuma taranmalı

- **Durgun deal'ler** — 14+ gündür aktivite yok → yeniden temas / aşağı çek / kaldır
- **Takılı deal'ler** — 30+ gündür aynı aşamada → zorla / çoklu kontak kur / eleme
- **Kapanış tarihi geçmiş** — tarihi güncelle / gelecek çeyreğe it / kaybedildi olarak kapat
- **Tek kontaklı deal'ler** — ek karar verici/etkileyici bul

## Hijyen Kontrolü

- Eksik kapanış tarihi
- Eksik tutar
- Eksik sonraki adım
- Birincil kontak atanmamış

## Kaldırılması Gereken Deal'ler

60+ gündür aktivite yok, 3+ kez ertelenmiş, şampiyon/destekleyici yok → "kaybedildi" olarak kapatmayı düşün. Ölü deal'ler pipeline'ı şişirir ve gerçek önceliği bulanıklaştırır.

## Uygulama notu

Bu değerlendirme [[crm_read]] script'inin desteklediği uçlarla (`deals/search`, `leads/search`, `outreach/search`) beslenmeli *(kaynak metinde "...py'nin desteklediği uçlarla" olarak kesik geldi, `crm_read.py`'ye atıf olduğu netti, öyle tamamlandı)*. Rakamlar/skorlar SADECE gerçek CRM verisinden hesaplanmalı — veri eksikse ("kapanış tarihi yok" gibi) bunu bir hijyen sorunu olarak raporla, tahmini rakam ÜRETME.
