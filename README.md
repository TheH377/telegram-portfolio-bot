# Telegram Portfolio Bot

A Telegram bot that presents my developer portfolio: a short bio, skill levels, projects, and contacts. The interface is available in English and Russian.

## Features

- Bilingual interface (English by default, Russian available via the 🌐 button)
- **About Me**: short introduction
- **Skills**: progress bars for each technology
- **Projects**: list of projects with links to GitHub
- **Contacts**: email, Telegram, and GitHub
- **Live demo**: secure password generator

## Project structure

```
├── bot.py              # Main bot logic
├── portfolio_data.py   # Profile, skills, and projects
├── texts.py            # Interface strings
├── requirements.txt    # Dependencies
├── .env                # Bot token (not committed)
└── .gitignore
```

## Getting started

1. Clone the repository and create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project folder:
   ```
   BOT_TOKEN=your_token_from_BotFather
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## Customization

Edit `portfolio_data.py` to change your name, skills, projects, and contacts. Edit `texts.py` to change interface strings.

## Built with

- Python 3
- [python-telegram-bot](https://python-telegram-bot.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)