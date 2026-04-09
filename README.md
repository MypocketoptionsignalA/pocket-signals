# Pocket Option OTC Signal Bot

This Telegram bot generates and sends BUY/SELL trading signals for Pocket Option OTC currency pairs every 1 minute.

## Features

- **Automated Signals**: Sends BUY/SELL alerts for USDJPY, GBPUSD, GBPJPY, EURUSD, and AUDUSD OTC pairs.
- **Customizable Interval**: Currently set to send a signal every 60 seconds.
- **Easy Setup**: Requires only a Telegram Bot Token and Chat ID.

## Prerequisites

- Python 3.7+
- `python-telegram-bot` library
- `ta` (Technical Analysis) library
- `pandas` library

## Installation

1. Clone this repository or download the files.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update the `TOKEN` and `CHAT_ID` in `main.py` with your own credentials.

## Usage

Run the bot using the following command:
```bash
python main.py
```

## Disclaimer

This bot is for educational purposes only. Trading involves risk, and signals are generated based on simulated logic. Always trade responsibly.
