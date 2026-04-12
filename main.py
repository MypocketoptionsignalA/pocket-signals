import asyncio
import logging
import random
from datetime import datetime
import pytz
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
TOKEN = os.getenv("BOT_TOKEN", "8704584052:AAEyEwepkfVjBEFvR02-zv7PXEWEX8LmFMI")

OTC_PAIRS = {
    "USD/JPY OTC": "🇯🇵🇺🇸",
    "GBP/USD OTC": "🇬🇧🇺🇸",
    "EUR/USD OTC": "🇪🇺🇺🇸",
    "AUD/USD OTC": "🇦🇺🇺🇸",
    "GBP/JPY OTC": "🇬🇧🇯🇵",
    "AUD/CAD OTC": "🇦🇺🇨🇦",
    "NZD/USD OTC": "🇳🇿🇺🇸",
    "EUR/GBP OTC": "🇪🇺🇬🇧",
    "USD/CAD OTC": "🇺🇸🇨🇦",
    "USD/CHF OTC": "🇺🇸🇨🇭",
    "EUR/JPY OTC": "🇪🇺🇯🇵",
    "CAD/JPY OTC": "🇨🇦🇯🇵",
    "AUD/NZD OTC": "🇦🇺🇳🇿",
    "GBP/AUD OTC": "🇬🇧🇦🇺",
    "EUR/AUD OTC": "🇪🇺🇦🇺",
}

SIGNAL_TIMEFRAMES = {
    "5s": "⚡", 
    "10s": "⏱️", 
    "15s": "⏳", 
    "30s": "🚀"
}

# Define the timezone for South Africa
SAST = pytz.timezone("Africa/Johannesburg")

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_signal(pair: str, timeframe: str) -> str:
    """Simulates generating an Ultra-Fast, high-impact BUY/SELL signal with color emojis."""
    signal_type = random.choice(["BUY", "SELL"])
    
    if signal_type == "BUY":
        signal_emoji = "🟢 BUY SIGNAL! 🟢"
    else:
        signal_emoji = "🔴 SELL SIGNAL! 🔴"

    return (
        f"**{signal_emoji}**\n"
        f"**Asset:** {pair} 💎\n"
        f"**Expiry:** {timeframe} ⏱️\n"
        f"**Action:** Enter NOW! 🔥"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with inline buttons for OTC pairs in a square layout with emojis."""
    keyboard = []
    pair_names = list(OTC_PAIRS.keys())
    for i in range(0, len(pair_names), 2):
        row = []
        if i < len(pair_names):
            pair = pair_names[i]
            row.append(InlineKeyboardButton(f"{OTC_PAIRS[pair]} {pair}", callback_data=f"PAIR_{pair}"))
        if i + 1 < len(pair_names):
            pair = pair_names[i+1]
            row.append(InlineKeyboardButton(f"{OTC_PAIRS[pair]} {pair}", callback_data=f"PAIR_{pair}"))
        if row:
            keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("**Welcome to the Elite Signal Bot!** 💎🚀\n\nChoose your preferred **OTC Asset**:", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_pair_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the selected OTC pair and prompts for timeframe with emojis."""
    query = update.callback_query
    await query.answer()

    selected_pair = query.data.replace("PAIR_", "")
    context.user_data["selected_pair"] = selected_pair

    keyboard = [
        [InlineKeyboardButton(f"{SIGNAL_TIMEFRAMES[tf]} {tf}", callback_data=f"TF_{tf}")] for tf in SIGNAL_TIMEFRAMES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"You selected **{selected_pair}**. Now choose your **Expiry Time**:", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_timeframe_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the selected timeframe and sends the signal."""
    query = update.callback_query
    await query.answer()

    selected_timeframe = query.data.replace("TF_", "")
    selected_pair = context.user_data.get("selected_pair")

    if not selected_pair:
        await query.edit_message_text(text="Oops! It seems the asset was not selected. Please start again with /start.")
        return

    signal_message = await generate_signal(selected_pair, selected_timeframe)
    timestamp_sast = datetime.now(SAST).strftime("%Y-%m-%d %I:%M:%S %p SAST")
    
    full_message = (
        f"{signal_message}\n\n"
        f"_Generated at: {timestamp_sast}_"
    )

    await query.edit_message_text(text=full_message, parse_mode="Markdown")

    # Offer to choose another pair with square layout
    keyboard = []
    pair_names = list(OTC_PAIRS.keys())
    for i in range(0, len(pair_names), 2):
        row = []
        if i < len(pair_names):
            pair = pair_names[i]
            row.append(InlineKeyboardButton(f"{OTC_PAIRS[pair]} {pair}", callback_data=f"PAIR_{pair}"))
        if i + 1 < len(pair_names):
            pair = pair_names[i+1]
            row.append(InlineKeyboardButton(f"{OTC_PAIRS[pair]} {pair}", callback_data=f"PAIR_{pair}"))
        if row:
            keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Choose another **OTC Asset**:", reply_markup=reply_markup, parse_mode="Markdown")

def main() -> None:
    """Run the bot."""
    if not TOKEN:
        logger.error("No BOT_TOKEN found in environment variables!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_pair_selection, pattern="^PAIR_"))
    application.add_handler(CallbackQueryHandler(handle_timeframe_selection, pattern="^TF_"))

    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
