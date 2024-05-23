# Blaze Double Bot

---

## Description

This Python script automates the betting process on the Blaze Double website using Selenium and undetected-chromedriver. It monitors the game state, places bets according to a predefined strategy, and handles winnings and losses.

---

## Installation

```bash

pip install blaze-double-bot

```

## How to use the JSON file in the Blaze Double Bot

To use the Blaze Double Bot, you need to configure your credentials and other settings through a JSON file. Follow the instructions below to set up and use the bot:

1. **Create a `config.json` file** with the following content:

```json
{
    "username": "your blaze username",
    "password": "your blaze password",
    "bet_amount":,
    "stop_loss_ratio": ,
    "stop_win_ratio":,
    "strategies": {
        "red": [
            ["B", "R", "B", "R", "B"],
            ["B", "B", "B", "B", "B"]
        ],
        "black": [
            ["R", "B", "R", "B", "R"],
            ["R", "R", "R", "R", "R"]
        ]
    }
}

```

- **username**: Your username or email registered on Blaze Double.
- **password**: Your password to access Blaze Double.
- **bet_amount**: The amount of the bet to be placed in each round.
- **stop_loss_ratio**: The multiplication factor of the initial balance indicating the loss limit. The bot will stop betting if the balance drops below this limit.
- **stop_win_ratio**: The multiplication factor of the initial balance indicating the win limit. The bot will stop betting if the balance reaches or exceeds this limit.
- **strategies**: Pre-defined betting strategies with sequences of colors (black = "B", red = "R"). You can add as many strategies as you want here.

2. **Create a `blazeBot.py` file** with the following content:

```python

from blaze_double_bot import BlazeDoubleBot

import json

with open('config.json', 'r') as f:
        config = json.load(f)

bot = BlazeDoubleBot(config)

bot.run()

```
#For each round won or lost, the bot will only perform the analyzes again after 5 rounds. The bot follows MartinGale's strategy of doubling the bet after a loss. He will repeat this procedure 2 times, or 1 time if he wins.
---

## Support This Project

If you find this project helpful, consider supporting it by making a donation. Your contribution will help me maintain and improve this bot.

[Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=928TRAX74TYSA)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

© 2024 Rafael Ribeiro.
