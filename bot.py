import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = """Eres el asistente personal de Lucciano, dueño de Glowraskin (glowraskin.co).
Glowraskin vende el Red Peel Serum AHA 30% + BHA 2% a $25 USD con envío gratis a EE.UU.

Tu trabajo es ayudarlo con todo lo relacionado a su negocio:
- Estrategia de TikTok y contenido viral
- Gestión de su tienda Shopify
- Ideas de videos, hooks y scripts
- Responder preguntas de clientes
- Marketing, SEO y conversión
- Cualquier tarea del día a día

Eres directo, creativo, hablas en español chileno relajado y conoces la tienda a fondo.
Cuando te pregunten algo del negocio, responde con foco en ventas y resultados reales."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔴 Hola Lucciano! Soy tu asistente de Glowraskin.\n\n"
        "Estoy aquí para ayudarte con TikTok, la tienda, videos, marketing y todo lo que necesites.\n\n"
        "¿En qué te ayudo?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("⏳ Un segundo...")
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.content[0].text
    except Exception as e:
        reply = f"Hubo un error: {str(e)}"
    await update.message.reply_text(reply)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
