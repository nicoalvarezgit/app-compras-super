import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

#bot_token=os.getenv('BOT_TOKEN')
bot_token = '7161967766:AAGC-Q6BHJG2iHftUcSI4026_T39ijA-iqw'

#Lista de productos a consultar
PRODUCTOS= ["arroz", "fideos", "jabón de tocador"]
RESPUESTAS={} #diccionario para guardar las respuestas

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía un mensaje inicial al usuario."""
    user=update.effective_user
    RESPUESTAS[user.id] = {} #Inicializa respuestas para este usuario
    await update.message.reply_text(f"Hola {user.first_name}! Vamos a revisar tu alacena.")
    await preguntar_producto(update, context)

async def preguntar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe la respuesta del usuario y avanza al siguiente producto."""
    index = context.user_data.get('producto_index', 0)  # Obtiene el índice actual (por defecto 0)
    if index < len(PRODUCTOS):
        producto= PRODUCTOS[index]
        await update.message.reply_text(f"Cuántos artículos de {producto} tenés?")
        context.user_data['producto_index'] = index + 1
    else:
        await update.message.reply_text(f"Gracias, terminamos por ahora")
        print(RESPUESTAS)  # Imprime las respuestas para depuración


async def manejar_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe la respuesta del usuario y avanza al siguiente producto."""
    user=update.effective_user
    texto=update.message.text

    #Validar si es un número
    if texto.isdigit():
        index= context.user_data.get('producto_index', 0)
        
        # Verificar si aún quedan productos por procesar
        if index < len(PRODUCTOS):
            producto = PRODUCTOS[index]
            RESPUESTAS[user.id][producto] = int(texto)  # Almacena la respuesta
            context.user_data['producto_index'] = index + 1  # Avanza al siguiente índice
            await preguntar_producto(update, context)
        else:
            await update.message.reply_text("Ya procesamos todos los productos. ¡Gracias!")
    else:
        await update.message.reply_text("Por favor, respondé con un número.")
        

#Configuración del bot
app = ApplicationBuilder().token(bot_token).build()

#Comandos y manejadores
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_respuesta))

#Ejecutar el bot
if __name__ == "__main__":
    print("El bot está corriendo...")
    app.run_polling()