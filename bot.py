import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

def get_services_keyboard():
    """Create an inline keyboard with salon services"""
    keyboard = InlineKeyboardMarkup()
    # Add buttons for each service with their respective callback data
    keyboard.row(
        InlineKeyboardButton("Haircut 💇", callback_data="service_haircut")
    )
    keyboard.row(
        InlineKeyboardButton("Coloring 🎨", callback_data="service_coloring")
    )
    keyboard.row(
        InlineKeyboardButton("Smoothening ✨", callback_data="service_smoothening")
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
    service = call.data.split('_')[1]
    response = f"You've selected {service.capitalize()}!"
    
    # Update the message to show the selection
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"{response}\n\nNext step: Implement date/time selection."
    )
    
    # Answer the callback query to remove the loading state
    bot.answer_callback_query(call.id)


bot.infinity_polling()