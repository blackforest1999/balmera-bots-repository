import os
import time
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Set this in Railway/Fly.io/Koyeb
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this to your deployed app's URL

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN and WEBHOOK_URL must be set as environment variables!")

bot = telebot.TeleBot(TOKEN)

# Define admin IDs
ADMINS = {
    "✨Theo✨": 7423845805,
    "✨Rang✨": 5719298294,
    "✨Lexa✨": 6571023283
}

# Store user-selected admin
user_admin_selection = {}
user_started = set()

# Initialize Flask
app = Flask(__name__)

# Webhook handler
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in user_started:
        welcome_text = "هــای دوست کوچولوی من! 🌸✨ خوش اومدی به دنیای جادویی بالمرا! اینجا می‌تونی حرفات رو کاملاً ناشناس با شورای قلمرو درمیون بذاری. " \
                       "بدون نگرانی صحبت کن، ما اینجاییم که گوش کنیم! 💌😊"
        bot.send_message(message.chat.id, welcome_text)
        user_started.add(message.chat.id)
    show_admin_selection(message.chat.id)

# Show admin selection
def show_admin_selection(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for admin in ADMINS.keys():
        markup.add(KeyboardButton(admin))
    bot.send_message(chat_id, "یک مدیر را برای ارسال پیام انتخاب کنید ✨😊", reply_markup=markup)

# Handle admin selection
@bot.message_handler(func=lambda message: message.text in ADMINS.keys())
def select_admin(message):
    user_admin_selection[message.chat.id] = ADMINS[message.text]
    bot.send_message(message.chat.id, "پیام ناشناس خود را ارسال کنید 📩🤍", reply_markup=ReplyKeyboardRemove())

# Forward messages to admin
@bot.message_handler(content_types=['text', 'photo', 'video', 'audio', 'document', 'voice', 'sticker', 'animation'])
def forward_message(message):
    if message.chat.id in user_admin_selection:
        admin_id = user_admin_selection[message.chat.id]
        user_mention = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        bot.send_message(admin_id, f"🔹 پیام از  {user_mention}:")
        
        if message.text:
            bot.send_message(admin_id, message.text)
        elif message.photo:
            bot.send_photo(admin_id, message.photo[-1].file_id, caption=message.caption)
        elif message.video:
            bot.send_video(admin_id, message.video.file_id, caption=message.caption)
        elif message.audio:
            bot.send_audio(admin_id, message.audio.file_id, caption=message.caption)
        elif message.document:
            bot.send_document(admin_id, message.document.file_id, caption=message.caption)
        elif message.voice:
            bot.send_voice(admin_id, message.voice.file_id)
        elif message.sticker:
            bot.send_sticker(admin_id, message.sticker.file_id)
        elif message.animation:
            bot.send_animation(admin_id, message.animation.file_id, caption=message.caption)
        
        bot.send_message(message.chat.id, "پیام شما ارسال شد ✅😊")
        show_admin_selection(message.chat.id)

# Remove and set webhook on startup
@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

# Run Flask server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
