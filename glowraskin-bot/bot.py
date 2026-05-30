import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not TELEGRAM_TOKEN:
    raise ValueError("ERROR: Variable TELEGRAM_TOKEN no esta configurada en Railway")
if not ANTHROPIC_API_KEY:
    raise ValueError("ERROR: Variable ANTHROPIC_API_KEY no esta configurada en Railway")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres el asistente personal de Lucciano, dueno de Glowraskin (glowraskin.co).
Glowraskin vende el Red Peel Serum AHA 30% + BHA 2% a $25 USD con envio gratis a EE.UU.

Tu trabajo es ayudarlo con todo lo relacionado a su negocio:
- Estrategia de TikTok y contenido viral
- Gestion de su tienda Shopify
- Ideas de videos, hooks y scripts
- Responder preguntas de clientes
- Marketing, SEO y conversion
- Cualquier tarea del dia a dia

Eres directo, creativo, hablas en espanol chileno relajado y conoces la tienda a fondo.
Cuando te pregunten algo del negocio, responde con foco en ventas y resultados reales."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola Lucciano! Soy tu asistente de Glowraskin.\n\n"
        "Estoy aqui para ayudarte con TikTok, la tienda, videos, marketing y todo lo que necesites.\n\n"
        "En que te ayudo?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Mensaje recibido: {user_message[:50]}")
    
    thinking_msg = await update.message.reply_text("Un segundo...")
    
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.content[0].text
        logger.info("Respuesta de Claude OK")
    except Exception as e:
        reply = f"Hubo un error al consultar a Claude: {str(e)}"
        logger.error(f"Error Claude: {e}")
    
    await thinking_msg.delete()
    await update.message.reply_text(reply)


def main():
    logger.info("Iniciando bot de Glowraskin...")
    logger.info(f"Token presente: {'SI' if TELEGRAM_TOKEN else 'NO'}")
    logger.info(f"API Key presente: {'SI' if ANTHROPIC_API_KEY else 'NO'}")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot corriendo correctamente!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
