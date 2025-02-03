
import time
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Replace with your bot token
TOKEN = '7713104021:AAGrN-RzrwSZ4DkmUOgbEjNlfheda6aqZvE'
WEBHOOK_URL = 'https://fashionable-leodora-blackforest-29005d4b.koyeb.app/SecretTalker_bot'

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
@app.route('/SecretTalker_bot', methods=['POST'])
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
        markup.add(KeyboardButton(admin))  # Use KeyboardButton instead of InlineKeyboardButton
    bot.send_message(chat_id, "یک مدیر را برای ارسال پیام انتخاب کنید ✨😊", reply_markup=markup)

# Handle admin selection
@bot.message_handler(func=lambda message: message.text in ADMINS.keys())
def select_admin(message):
    user_admin_selection[message.chat.id] = ADMINS[message.text]
    bot.send_message(message.chat.id, "پیام ناشناس خود را ارسال کنید 📩🤍", reply_markup=ReplyKeyboardRemove())

# Forward message to admin
@bot.message_handler(func=lambda message: message.chat.id in user_admin_selection)
def forward_message(message):
    admin_id = user_admin_selection[message.chat.id]
    user_mention = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    bot.send_message(admin_id, f"🔹 پیام از  {user_mention}:")
    bot.send_message(admin_id, message.text)

    bot.send_message(message.chat.id, "پیام شما ارسال شد ✅😊")
    show_admin_selection(message.chat.id)

# Set webhook
bot.remove_webhook()
time.sleep(1)  # Sleep to avoid hitting rate limits
bot.set_webhook(url=WEBHOOK_URL)

# Run Flask server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
