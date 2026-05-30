import os
import time
import requests
import anthropic

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres el asistente personal de Lucciano, dueno de Glowraskin (glowraskin.co).
Glowraskin vende el Red Peel Serum AHA 30% + BHA 2% a $25 USD con envio gratis a EE.UU.
Tu trabajo es ayudarlo con todo lo relacionado a su negocio:
- Estrategia de TikTok y contenido viral
- Gestion de su tienda Shopify
- Ideas de videos, hooks y scripts
- Marketing, SEO y conversion
- Cualquier tarea del dia a dia
Eres directo, creativo, hablas en espanol chileno relajado y conoces la tienda a fondo."""

def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    try:
        r = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=35)
        return r.json().get("result", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def ask_claude(message):
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Bot Glowraskin iniciando...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            if not chat_id or not text:
                continue
            if text == "/start":
                send_message(chat_id, "Hola Lucciano! Soy tu asistente de Glowraskin. En que te ayudo?")
                continue
            print(f"Mensaje: {text[:50]}")
            send_message(chat_id, "Un segundo...")
            reply = ask_claude(text)
            send_message(chat_id, reply)
        time.sleep(1)

if __name__ == "__main__":
    main()
