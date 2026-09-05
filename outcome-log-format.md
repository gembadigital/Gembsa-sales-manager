# outcome-log.jsonl — Format Notu

*Faz 2 (Seçenek A) — CRM şeması değişmeden, workspace içi sonuç geri beslemesi. Bkz. `gemba-sales-coaching-plan.md`.*

`outcome-log.jsonl` workspace kökünde, JSON Lines formatında bir dosyadır — her satır bağımsız bir JSON obje, satırlar asla silinmez/üzerine yazılmaz, sadece append edilir.

## Satır şeması

```json
{"date": "2026-09-05", "company": "Retay Arms", "dealId": null, "draftType": "yeniden_temas", "outcome": "positive", "note": "Toplantı çıktı, Perşembe görüşülecek."}
```

| Alan | Zorunlu mu | Açıklama |
|---|---|---|
| `date` | evet | Atakan'ın sonucu bildirdiği tarih, `YYYY-MM-DD` |
| `company` | evet | Şirket adı — Atakan'ın mesajındaki adla, CRM'deki kayıtlı adla mümkünse aynı yazımda |
| `dealId` | hayır (`null` olabilir) | CRM'deki deal/outreach id'si biliniyorsa/kolayca bulunuyorsa doldurulur; bunun için ekstra bir CRM taraması ZORUNLU değildir |
| `draftType` | evet | `ilk_temas` \| `yeniden_temas` \| `itiraz_yaniti` \| `ad-hoc` \| `diger` |
| `outcome` | evet | `positive` \| `negative` \| `neutral` |
| `note` | evet (kısa) | Atakan'ın verdiği kısa serbest metin (ör. "toplantı çıktı", "cevap gelmedi", "ilgilenmiyor dedi") |

## Kurallar

- Sadece Atakan'ın Telegram'dan (interaktif chat) gerçekten bildirdiği sonuçlar kaydedilir — tahmin/varsayım yazılmaz (DÜRÜSTLÜK VE DOĞRULAMA İLKESİ).
- Şirket/kayıt eşleşmesi belirsizse (aynı isimli birden fazla aday/deal olabilir), kaydetmeden önce Atakan'a netleştirici soru sorulur.
- Yazıldıktan sonra dosya gerçekten okunarak (append edilen satır göründüğü) doğrulanır, sonra Telegram'dan "kaydettim: ..." diye teyit edilir.
- Bu dosya CRM şemasını değiştirmez; CRM tarafında kalıcı bir `outcome` alanı ihtiyacı hâlâ ayrı bir konu olarak duruyor (Faz 2 Seçenek B, dev-team backlog).
