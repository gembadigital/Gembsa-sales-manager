#!/usr/bin/env python3
"""Bagimsiz butunluk kontrolu - TUM korumali script'ler icin (genellestirilmis).

gemba-sales-manager ajaninin kendi gorev dongusunden TAMAMEN BAGIMSIZ
calisir; sistem crontab'i tarafindan tetiklenir (bkz. `crontab -l`).

Korunan script listesi `protected-scripts.json` manifestinden okunur -
kod icinde tek tek isimlendirilmez. Yeni bir korumali script eklemek icin
sadece manifest dosyasina bir satir eklemek yeterlidir (bkz. o dosyadaki
_comment alani).

Her script icin hash sapmasi tespit edilirse:
  1. O script'in exec-approvals allowlist girdisini (manifestte
     allowlist_entry_id doluysa) OTOMATIK kaldirir - script tekrar
     ask=on-miss ile onay gerektirir hale gelir. allowlist_entry_id null
     ise (script hic allowlist'te degilse) bu adim atlanir.
  2. Telegram'a (gemba-sales-manager ajani uzerinden) hangi script'in
     etkilendigini belirten bir uyari gonderir.
  3. Olayi yerel bir denetim gunlugune yazar.

Sapma cozulup dosya orijinal haline donerse (hash tekrar eslesirse),
sadece o script icin "alerted" isaretini temizler - allowlist girdisini
GERI EKLEMEZ. Allowlist'i yeniden acmak kasitli olarak MANUEL bir
adimdir (Atakan/operator inceleyip `openclaw approvals allowlist add ...`
ya da `openclaw approvals set --file ...` calistirmali).

Bu mekanizma SADECE dosya BUTUNLUGUNU (icerik degisikligi) tespit eder -
onay ekraninda komut metninin (`commandText`) script'in o anki icerigini
GOSTERMEDIGI icin (2026-09-03 tts_voice_reply.py olayinda kanitlandi:
Atakan "python3 tts_voice_reply.py && rm ..." komutunu onayladi ama
script'in bir saniye once ElevenLabs kullanan sahte bir versiyonla
degistirildigini onay ekrani hic gostermedi), bu bagimsiz kontrol
approval akisindan AYRI, ek bir koruma katmanidir.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace-gemba-sales")
MANIFEST_FILE = WORKSPACE / "protected-scripts.json"
ALERTED_MARKER_FILE = WORKSPACE / ".protected-scripts.drift-alerted.json"
AUDIT_LOG = WORKSPACE / ".protected-scripts.integrity-log"

AGENT_ID = "gemba-sales-manager"
TELEGRAM_ACCOUNT = "gemba-iq"
TELEGRAM_TARGET = "8540345447"


def log(line: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    with open(AUDIT_LOG, "a") as f:
        f.write(f"{ts} {line}\n")


def load_manifest() -> dict:
    if not MANIFEST_FILE.exists():
        log("HATA: protected-scripts.json bulunamadi, kontrol atlaniyor")
        return {}
    data = json.loads(MANIFEST_FILE.read_text())
    return data.get("scripts", {})


def load_alerted() -> dict:
    if not ALERTED_MARKER_FILE.exists():
        return {}
    try:
        return json.loads(ALERTED_MARKER_FILE.read_text())
    except Exception:
        return {}


def save_alerted(alerted: dict) -> None:
    ALERTED_MARKER_FILE.write_text(json.dumps(alerted, indent=2))


def current_hash(filename: str) -> str | None:
    path = WORKSPACE / filename
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_allowlist_entry(entry_id: str) -> bool:
    """exec-approvals config'inden sadece verilen id'li girdiyi kaldirir."""
    try:
        raw = subprocess.run(
            ["openclaw", "approvals", "get", "--json"],
            capture_output=True, text=True, timeout=30, check=True,
        ).stdout
    except Exception as e:
        log(f"HATA: approvals get basarisiz: {e}")
        return False

    json_line = None
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{") and '"file"' in line:
            json_line = line
            break
    if not json_line:
        log("HATA: approvals get ciktisinda JSON satiri bulunamadi")
        return False

    data = json.loads(json_line)
    cfg = data["file"]
    agent_cfg = cfg.get("agents", {}).get(AGENT_ID)
    if not agent_cfg:
        log(f"HATA: config'te '{AGENT_ID}' ajani bulunamadi")
        return False

    before = len(agent_cfg.get("allowlist", []))
    agent_cfg["allowlist"] = [
        e for e in agent_cfg.get("allowlist", [])
        if e.get("id") != entry_id
    ]
    after = len(agent_cfg["allowlist"])
    if before == after:
        log(f"UYARI: allowlist id={entry_id} zaten yoktu (before==after=={before})")
        return True

    tmp_path = WORKSPACE / ".exec-approvals-driftfix.json"
    tmp_path.write_text(json.dumps(cfg, indent=2))
    try:
        subprocess.run(
            ["openclaw", "approvals", "set", "--file", str(tmp_path)],
            capture_output=True, text=True, timeout=30, check=True,
        )
    except Exception as e:
        log(f"HATA: approvals set basarisiz: {e}")
        return False
    finally:
        tmp_path.unlink(missing_ok=True)

    log(f"allowlist guncellendi: id={entry_id} kaldirildi ({before} -> {after} kayit)")
    return True


def send_telegram_alert(script_name: str, old_hash: str | None, new_hash: str | None) -> None:
    message = (
        f"GUVENLIK UYARISI: '{script_name}' butunluk kontrolu basarisiz oldu.\n"
        f"Beklenen hash: {old_hash}\n"
        f"Bulunan hash: {new_hash}\n"
        "Dosya beklenmedik sekilde degismis olabilir. Allowlist'te bir "
        "girdisi varsa OTOMATIK olarak kaldirildi (artik tekrar onay "
        "istiyor). Lutfen dosyayi inceleyin; sorun yoksa hash'i "
        "protected-scripts.json'da guncelleyip allowlist'i manuel olarak "
        "yeniden acin."
    )
    system_note = (
        "SISTEM NOTU (agent icin, Telegram'a gonderme): bu mesaj bagimsiz bir "
        "butunluk kontrolunden geliyor, bir script'in gecerliligi sorgulaniyor. "
        "Bu mesaji aldiginda dosyayi OKUYABILIRSIN ama KESINLIKLE DUZENLEME/"
        "SILME/YENIDEN OLUSTURMA yapma ve allowlist'i kendin geri acma - bu "
        "karar SADECE Atakan'a ait. Tek gorevin: asagidaki metni AYNEN, "
        "hicbir yorum/analiz/aksiyon eklemeden Telegram'a ilet."
    )
    try:
        subprocess.run(
            [
                "openclaw", "agent",
                "--agent", AGENT_ID,
                "--message", f"{system_note}\n\n---\n{message}",
                "--deliver",
                "--reply-channel", "telegram",
                "--reply-account", TELEGRAM_ACCOUNT,
                "--reply-to", TELEGRAM_TARGET,
            ],
            capture_output=True, text=True, timeout=120, check=True,
        )
        log(f"Telegram uyarisi gonderildi: {script_name}")
    except Exception as e:
        log(f"HATA: Telegram uyarisi gonderilemedi ({script_name}): {e}")


def main() -> int:
    manifest = load_manifest()
    if not manifest:
        return 1

    alerted = load_alerted()
    any_drift = False
    changed_alerted = False

    for script_name, info in manifest.items():
        expected = info.get("sha256")
        entry_id = info.get("allowlist_entry_id")
        found = current_hash(script_name)

        if found == expected:
            if script_name in alerted:
                del alerted[script_name]
                changed_alerted = True
                log(f"'{script_name}': hash tekrar eslesti, drift-alerted isareti temizlendi (allowlist MANUEL yeniden acilmali)")
            continue

        any_drift = True
        if script_name in alerted:
            continue

        log(f"'{script_name}': SAPMA TESPIT EDILDI: beklenen={expected} bulunan={found}")
        if entry_id:
            remove_allowlist_entry(entry_id)
        else:
            log(f"'{script_name}': allowlist girdisi yok (allowlist_entry_id=null), kaldirilacak bir sey yok")
        send_telegram_alert(script_name, expected, found)
        alerted[script_name] = {
            "detected_at": datetime.now(timezone.utc).isoformat(),
            "expected": expected,
            "found": found,
        }
        changed_alerted = True

    if changed_alerted:
        save_alerted(alerted)

    return 1 if any_drift else 0


if __name__ == "__main__":
    sys.exit(main())
