#!/usr/bin/env python3
"""Metin -> Turkce sesli mesaj (OGG/Opus) uretme koprusu.

Telegram'a GONDERMEZ - sadece ses dosyasi uretir. Gonderim, canli ajanin
kendi mesaj gonderme aracindan (audioAsVoice mekanizmasi) yapilir, cunku
`openclaw message send` bu kurulumda coklu-ajan sahiplik hatasi nedeniyle
calismiyor (2026-09-02'de mail gonderiminde de ayni sorun bulunmustu).

SADECE yerel Piper TTS kullanir - ElevenLabs/OpenAI/baska bir ucretli
API'ye ASLA bagimli degildir ve olmamalidir (butce kisiti).

Ses: sabit olarak Fahrettin (tr_TR-fahrettin-medium) - Atakan 2026-09-03'te
bunu secti, Fettah modeli diskten silindi. Tek ses oldugu icin script bir
ses parametresi GEREKTIRMEZ.

Kullanim: python3 tts_voice_reply.py
Geriye donuk uyumluluk: eski "fahrettin"/"fettah" argumaniyla cagrilirsa
(agent'in eski arayuzu hatirlayip kullanmasi ihtimaline karsi - bu
gercekten yasandi, 2026-09-03) HATA VERMEZ, sessizce yok sayilir ve yine
tek ses (fahrettin) kullanilir.
Metin, ayni dizindeki tts_input.txt dosyasindan okunur.
Cikti, her zaman sabit bir dosyaya yazilir: voice_reply.ogg
"""
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
MODEL = Path("/opt/piper/voices/tr_TR-fahrettin-medium.onnx")
PIPER_BIN = "/opt/piper/piper/piper"
# Konusma hizi (Piper --length_scale, varsayilan 1.0 = normal). Atakan
# fahrettin'in hizli geldigini belirtti (2026-09-03) - 1.15 ile ~%8
# yavaslatildi, onayladi.
LENGTH_SCALE = 1.15
INPUT_FILE = WORKSPACE / "tts_input.txt"
WAV_OUT = WORKSPACE / "voice_reply.wav"
OGG_OUT = WORKSPACE / "voice_reply.ogg"


LEGACY_VOICE_ARGS = {"fahrettin", "fettah"}


def main():
    if len(sys.argv) not in (1, 2):
        print("Kullanim: python3 tts_voice_reply.py (parametre gerektirmez)", file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 2 and sys.argv[1] not in LEGACY_VOICE_ARGS:
        print(f"REDDEDILDI: bilinmeyen parametre '{sys.argv[1]}'.", file=sys.stderr)
        sys.exit(1)
    # len(sys.argv) == 2 ve LEGACY_VOICE_ARGS icindeyse: sessizce yok say,
    # asagida devam et (tek ses zaten fahrettin).

    if not INPUT_FILE.exists():
        print(f"REDDEDILDI: {INPUT_FILE} bulunamadi - once metni bu dosyaya yaz.", file=sys.stderr)
        sys.exit(1)

    text = INPUT_FILE.read_text(encoding="utf-8").strip()
    if not text:
        print("REDDEDILDI: girdi metni bos.", file=sys.stderr)
        sys.exit(1)

    if not MODEL.exists():
        print(f"REDDEDILDI: model dosyasi bulunamadi: {MODEL}", file=sys.stderr)
        sys.exit(1)

    piper_proc = subprocess.run(
        [PIPER_BIN, "-m", str(MODEL), "-f", str(WAV_OUT),
         "--length_scale", str(LENGTH_SCALE)],
        input=text, capture_output=True, text=True,
    )
    if piper_proc.returncode != 0:
        print(f"HATA (piper): {piper_proc.stderr}", file=sys.stderr)
        sys.exit(1)

    ffmpeg_proc = subprocess.run(
        ["ffmpeg", "-y", "-i", str(WAV_OUT), "-c:a", "libopus", "-b:a", "32k", str(OGG_OUT)],
        capture_output=True, text=True,
    )
    if ffmpeg_proc.returncode != 0:
        print(f"HATA (ffmpeg): {ffmpeg_proc.stderr[-500:]}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {OGG_OUT} uretildi.")


if __name__ == "__main__":
    main()
