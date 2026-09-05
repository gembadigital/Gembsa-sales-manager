#!/bin/bash
# Anthropic API key'ini guvenli sekilde toplar ve OpenClaw'a baglar.
# Key EKRANA YAZILMAZ (read -s), dosyaya (chmod 600) yazilir, openclaw.json'a
# DUZ METIN olarak GOMULMEZ - iki adimli bir SecretRef (source: file) ile
# dosya yoluna referans verilir (Google'in mevcut duz-metin deseninden daha
# guvenli): once secrets.providers.anthropic_key adinda bir "file" saglayici
# tanimlanir, sonra models.providers.anthropic.apiKey buna referans verir.
set -euo pipefail

WORKSPACE="/root/.openclaw/workspace-gemba-sales"
KEY_FILE="$WORKSPACE/anthropic-api-key.txt"
GITIGNORE="$WORKSPACE/.gitignore"

echo "Anthropic API key'i girin (ekranda gorunmeyecek):"
read -s -p "Anthropic API key: " ANTHROPIC_API_KEY
echo

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "REDDEDILDI: bos deger girildi." >&2
  unset ANTHROPIC_API_KEY
  exit 1
fi

# 1) Dosyaya yaz, hemen kilitle (var olan gemba-iq-api-key.txt ile ayni desen:
#    duz metin, trailing newline yok, chmod 600)
printf '%s' "$ANTHROPIC_API_KEY" > "$KEY_FILE"
chmod 600 "$KEY_FILE"
echo "OK: key $KEY_FILE dosyasina yazildi (chmod 600)."

# Artik shell degiskenine ihtiyac yok - dosyadan okunacak
unset ANTHROPIC_API_KEY

# 2) .gitignore teyidi
if grep -qxF "anthropic-api-key.txt" "$GITIGNORE" 2>/dev/null; then
  echo "OK: anthropic-api-key.txt zaten .gitignore'da."
else
  sed -i '/^gemba-iq-api-key\.txt$/a anthropic-api-key.txt' "$GITIGNORE"
  echo "OK: anthropic-api-key.txt .gitignore'a eklendi."
fi

if git -C "$WORKSPACE" ls-files --error-unmatch anthropic-api-key.txt >/dev/null 2>&1; then
  echo "UYARI: anthropic-api-key.txt git tarafindan takip ediliyor! Bu ciddi bir sorun - hemen bildirin." >&2
else
  echo "OK: anthropic-api-key.txt git tarafindan hic takip edilmiyor."
fi

# 3) OpenClaw config: once dosya-tabanli named secret provider tanimla...
openclaw config set secrets.providers.anthropic_key \
  --provider-source file \
  --provider-path "$KEY_FILE" \
  --provider-mode singleValue

# ...sonra models.providers.anthropic.apiKey bu saglayiciya REFERANS versin
# (duz key degeri openclaw.json'a hic yazilmiyor)
openclaw config set models.providers.anthropic.apiKey \
  --ref-provider anthropic_key \
  --ref-source file \
  --ref-id value

openclaw config set models.providers.anthropic.api "anthropic-messages"

# 4) gemba-sales-manager icin model/fallback: birincil Anthropic, Google'lar fallback kalsin
openclaw config set agents.entries.gemba-sales-manager.modelPolicy.allow \
  '["google/gemini-2.5-flash","google/gemini-3-flash-preview","anthropic/claude-sonnet-5"]' \
  --strict-json --replace

openclaw config set agents.entries.gemba-sales-manager.model.primary "anthropic/claude-sonnet-5"
openclaw config set agents.entries.gemba-sales-manager.model.fallbacks \
  '["google/gemini-3-flash-preview","google/gemini-3.5-flash","google/gemini-3.1-flash-lite","google/gemini-3.5-flash-lite","google/gemini-3.1-pro-preview"]' \
  --strict-json --replace

echo "OK: openclaw.json guncellendi (models.providers.anthropic SecretRef ile, gemba-sales-manager model/fallback)."
echo "Kurulum tamamlandi. Anahtar hicbir noktada ekrana/log'a yazdirilmadi."
