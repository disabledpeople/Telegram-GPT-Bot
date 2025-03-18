import telebot
import openai
import logging

# Конфигурация
TELEGRAM_TOKEN = "ТВОЙ_ТОКЕН_БОТА"
OPENAI_API_KEY = "ТВОЙ_КЛЮЧ_OPENAI"
ALLOWED_USERS = {TELEGRAM_id, TELEGRAM_id}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Настройка логирования
logging.basicConfig(filename="bot_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id in ALLOWED_USERS:
        bot.send_message(message.chat.id, "Привет! Я бот ChatGPT. Задавай вопросы!")
    else:
        bot.send_message(message.chat.id, "Извините, доступ к боту ограничен.")

@bot.message_handler(func=lambda message: message.from_user.id in ALLOWED_USERS)
def chat_with_gpt(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message.content
        
        bot.send_message(message.chat.id, reply)

        # Логирование
        log_entry = f"USER [{message.from_user.id}]: {message.text}\nBOT: {reply}\n"
        logging.info(log_entry)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: " + str(e))
        logging.error(f"Ошибка: {e}")

@bot.message_handler(func=lambda message: True)
def deny_access(message):
    bot.send_message(message.chat.id, "Извините, доступ к боту ограничен.")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
