import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store service details
SERVICES = {
    'haircut': {
        'name': 'Haircut',
        'price': 100,
        'emoji': '💇'
    },
    'coloring': {
        'name': 'Coloring',
        'price': 500,
        'emoji': '🎨'
    },
    'smoothening': {
        'name': 'Smoothening',
        'price': 350,
        'emoji': '✨'
    },
    'beard': {
        'name': 'Beard Trim',
        'price': 100,
        'emoji': '🧏‍♂️'
    }
}

def get_services_keyboard():
    """Create an inline keyboard with salon services and their prices"""
    keyboard = InlineKeyboardMarkup()
    
    # Add buttons for each service with their respective callback data and prices
    for service_id, details in SERVICES.items():
        button_text = f"{details['name']} {details['emoji']} - ₹{details['price']}"
        keyboard.row(
            InlineKeyboardButton(
                button_text, 
                callback_data=f"service_{service_id}"
            )
        )
    return keyboard

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to our Salon Booking Bot! 💅\nHow can we help you today?")
    show_services_menu(message)

@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = """
This bot lets you book your salon appointment. 
Select which type of service you would like from the menu below.
Then select the available date and time slot.
    """
    bot.reply_to(message, help_text)
    show_services_menu(message)

def show_services_menu(message):
    """Display the services menu"""
    bot.send_message(
        message.chat.id,
        "Please select a service:",
        reply_markup=get_services_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def handle_service_selection(call):
    """Handle service selection callbacks"""
    service_id = call.data.split('_')[1]
    service = SERVICES[service_id]
    
    response = (
        f"You've selected {service['name']} {service['emoji']}\n"
        f"Price: ₹{service['price']}"
    )
    
    # Update the message to show the selection
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"{response}\n\nNext step: Implement date/time selection."
    )
    
    # Answer the callback query to remove the loading state
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    show_services_menu(message)

bot.infinity_polling()