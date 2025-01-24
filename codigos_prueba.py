import asyncio
from telegram import Bot

bot_token = '7161967766:AAGC-Q6BHJG2iHftUcSI4026_T39ijA-iqw'
bot = Bot(token=bot_token)

# Puedes obtener el chat ID enviando un mensaje al bot y luego consultando el ID usando el método getUpdates
chat_id = '5801580852'

# Enviar mensaje de prueba
async def send_message():
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text="¡Hola! Este es un mensaje de prueba de tu nuevo bot.")  # Await para enviar el mensaje

# Ejecutar la función asincrónica
asyncio.run(send_message())