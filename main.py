import asyncio
import logging
import random
from datetime import datetime
import pytz
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
TOKEN = os.getenv('BOT_TOKEN', '8704584052:AAEyEwepkfVjBEFvR02-zv7PXEWEX8LmFMI')

OTC_PAIRS = [
    'USDJPY OTC',
    'GBPUSD OTC',
    'GBPJPY OTC',
    'EURUSD OTC',
    'AUDUSD OTC',
]

SIGNAL_TIMEFRAMES = [
    '5s', '10s', '15s', '30s'
]

# Define the timezone for South Africa
SAST = pytz.timezone('Africa/Johannesburg')

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_signal(pair: str, timeframe: str) -> str:
    """Simulates generating a BUY/SELL signal for a given pair and timeframe."""
    signal_type = random.choice(['BUY', 'SELL'])
    return f"{signal_type} SIGNAL! 🔥\nEnter NOW ⏰ (Timeframe: {timeframe})"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with inline buttons for OTC pairs."""
    keyboard = [
        [InlineKeyboardButton(pair, callback_data=f"PAIR_{pair}")] for pair in OTC_PAIRS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an OTC pair:', reply_markup=reply_markup)

async def handle_pair_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the selected OTC pair and prompts for timeframe."""
    query = update.callback_query
    await query.answer()

    selected_pair = query.data.replace('PAIR_', '')
    context.user_data['selected_pair'] = selected_pair

    keyboard = [
        [InlineKeyboardButton(tf, callback_data=f"TF_{tf}")] for tf in SIGNAL_TIMEFRAMES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f'You selected {selected_pair}. Now choose a timeframe:', reply_markup=reply_markup)

async def handle_timeframe_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the selected timeframe and sends the signal."""
    query = update.callback_query
    await query.answer()

    selected_timeframe = query.data.replace('TF_', '')
    selected_pair = context.user_data.get('selected_pair')

    if not selected_pair:
        await query.edit_message_text(text='Oops! It seems the pair was not selected. Please start again with /start.')
        return

    signal_message = await generate_signal(selected_pair, selected_timeframe)
    timestamp_sast = datetime.now(SAST).strftime('%I:%M %p')
    message_text = f"{signal_message}\n\n📈 {selected_pair}\n{timestamp_sast}"

    await query.edit_message_text(text=f"Signal for {selected_pair} ({selected_timeframe}):\n{message_text}")

    # Offer to choose another pair
    keyboard = [
        [InlineKeyboardButton(pair, callback_data=f"PAIR_{pair}")] for pair in OTC_PAIRS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('Choose another OTC pair:', reply_markup=reply_markup)

def main() -> None:
    """Run the bot."""
    if not TOKEN:
        logger.error("No BOT_TOKEN found in environment variables!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_pair_selection, pattern='^PAIR_'))
    application.add_handler(CallbackQueryHandler(handle_timeframe_selection, pattern='^TF_'))

    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
