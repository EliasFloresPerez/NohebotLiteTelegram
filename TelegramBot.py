from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os


# Carga las variables de entorno del archivo .env
load_dotenv()


class BotTelegram:
    # Atributos
    token = os.getenv('TELEGRAMTOKEN')
    updater = Application.builder().token(token).build()

    # Guarda el chat_id del grupo aquí 
    grupo_chat_id = os.getenv('CHAT_ID')

    def __init__(self):
        pass

    async def send_message(self, chat_id: int, text: str) -> None:
        print(f"Enviando mensaje al chat")
        # Envía un mensaje al chat (en este caso, el grupo)
        await self.updater.bot.send_message(chat_id=chat_id, text=text,parse_mode= ParseMode.HTML) 

    def iniciar(self):
        self.updater.run_polling()

    


    
