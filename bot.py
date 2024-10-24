import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import calendar

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# [Previous service and time slots dictionaries remain the same]
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
    }
}

TIME_SLOTS = [
    "10:00 AM", "11:00 AM", "12:00 PM", 
    "1:00 PM", "2:00 PM", "3:00 PM", 
    "4:00 PM", "5:00 PM", "6:00 PM"
]

def get_services_keyboard():
    """Create an inline keyboard with salon services and their prices"""
    keyboard = InlineKeyboardMarkup()
    for service_id, details in SERVICES.items():
        button_text = f"{details['name']} {details['emoji']} - ₹{details['price']}"
        keyboard.row(
            InlineKeyboardButton(
                button_text, 
                callback_data=f"service_{service_id}"
            )
        )
    return keyboard

def create_calendar_keyboard(year, month):
    """Create a calendar keyboard for date selection"""
    keyboard = InlineKeyboardMarkup(row_width=7)
    
    # Add month and year display
    month_name = calendar.month_name[month]
    keyboard.row(
        InlineKeyboardButton(f"{month_name} {year}", callback_data="ignore")
    )
    
    # Add day names
    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    keyboard.row(*[InlineKeyboardButton(day, callback_data="ignore") for day in days])
    
    # Get the calendar for current month
    cal = calendar.monthcalendar(year, month)
    
    # Get current date for comparison
    current_date = datetime.now()
    
    # Add calendar days
    for week in cal:
        row_buttons = []
        for day in week:
            if day == 0:
                row_buttons.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                # Create date object for comparison
                date = datetime(year, month, day)
                
                # Only allow booking for future dates (including today)
                if date >= current_date.replace(hour=0, minute=0, second=0, microsecond=0):
                    row_buttons.append(
                        InlineKeyboardButton(
                            str(day),
                            callback_data=f"date_{year}_{month}_{day}"
                        )
                    )
                else:
                    row_buttons.append(
                        InlineKeyboardButton("✖", callback_data="ignore")
                    )
        keyboard.row(*row_buttons)
    
    # Calculate previous and next month/year
    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month = 12
        prev_year -= 1
        
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1
    
    # Only show previous month button if it's not in the past
    nav_buttons = []
    current_date = datetime.now()
    if datetime(prev_year, prev_month, 1) >= current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        nav_buttons.append(
            InlineKeyboardButton(
                "⬅️ Previous Month",
                callback_data=f"month_{prev_year}_{prev_month}"
            )
        )
    
    nav_buttons.append(
        InlineKeyboardButton(
            "Next Month ➡️",
            callback_data=f"month_{next_year}_{next_month}"
        )
    )
    
    # Add navigation buttons
    keyboard.row(*nav_buttons)
    
    return keyboard

def create_time_slots_keyboard(date_str):
    """Create a keyboard with available time slots"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = []
    
    for time_slot in TIME_SLOTS:
        buttons.append(
            InlineKeyboardButton(
                time_slot,
                callback_data=f"time_{date_str}_{time_slot}"
            )
        )
    
    # Add buttons in rows of 3
    for i in range(0, len(buttons), 3):
        keyboard.add(*buttons[i:i+3])
        
    # Add back button
    keyboard.row(
        InlineKeyboardButton("⬅️ Back to Calendar", callback_data="back_to_calendar")
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
1. Select your desired service
2. Choose a date from the calendar
3. Pick an available time slot
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
        f"Selected Service: {service['name']} {service['emoji']}\n"
        f"Price: ₹{service['price']}\n\n"
        f"Please select a date for your appointment:"
    )
    
    # Show calendar for date selection
    now = datetime.now()
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response,
        reply_markup=create_calendar_keyboard(now.year, now.month)
    )
    
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('month_'))
def handle_month_navigation(call):
    """Handle month navigation in calendar"""
    _, year, month = call.data.split('_')
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=create_calendar_keyboard(int(year), int(month))
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('date_'))
def handle_date_selection(call):
    """Handle date selection from calendar"""
    _, year, month, day = call.data.split('_')
    selected_date = f"{year}-{month}-{day}"
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Selected date: {day}/{month}/{year}\nPlease select a time slot:",
        reply_markup=create_time_slots_keyboard(selected_date)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('time_'))
def handle_time_selection(call):
    """Handle time slot selection"""
    _, date, time = call.data.split('_', 2)
    year, month, day = date.split('-')
    
    confirmation_text = (
        f"🎉 Great! Your appointment is scheduled for:\n"
        f"📅 Date: {day}/{month}/{year}\n"
        f"🕒 Time: {time}\n\n"
        f"We'll send you a reminder before your appointment.\n"
        f"Type /start to make another booking."
    )
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=confirmation_text
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_calendar')
def handle_back_to_calendar(call):
    """Handle back to calendar button"""
    now = datetime.now()
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Please select a date for your appointment:",
        reply_markup=create_calendar_keyboard(now.year, now.month)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def handle_ignore_callback(call):
    """Handle callbacks that should be ignored"""
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    show_services_menu(message)

bot.infinity_polling()