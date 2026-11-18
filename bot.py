import os
import secrets
import string
import logging

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from portfolio_data import PROFILE
from texts import TEXTS

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Язык, который открывается по умолчанию: "en" или "ru"
DEFAULT_LANG = "en"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# ---------- Язык ----------

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Возвращает язык текущего пользователя (или язык по умолчанию)."""
    return context.user_data.get("lang", DEFAULT_LANG)


def t(context: ContextTypes.DEFAULT_TYPE, key: str) -> str:
    """Берёт фразу из texts.py на нужном языке."""
    return TEXTS[get_lang(context)][key]


# ---------- Клавиатуры ----------

def main_menu(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(t(context, "about"), callback_data="about")],
        [InlineKeyboardButton(t(context, "skills"), callback_data="skills")],
        [InlineKeyboardButton(t(context, "projects"), callback_data="projects")],
        [InlineKeyboardButton(t(context, "password"), callback_data="password")],
        [InlineKeyboardButton(t(context, "contacts"), callback_data="contacts")],
        [InlineKeyboardButton(t(context, "switch_lang"), callback_data="toggle_lang")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_button(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(context, "back"), callback_data="menu")]]
    )


# ---------- Тексты разделов ----------

def format_skills(lang: str) -> str:
    lines = [TEXTS[lang]["skills_title"], ""]
    for name, level in PROFILE["skills"].items():
        filled = level // 10
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"{name}: {bar} {level}%")
    return "\n".join(lines)


def format_projects(lang: str) -> str:
    parts = []
    for project in PROFILE["projects"]:
        parts.append(
            f"📁 {project['title']}\n"
            f"{project['description'][lang]}\n"
            f"{TEXTS[lang]['stack']}: {project['stack']}\n"
            f"{project['link']}"
        )
    return "\n\n".join(parts)


def format_contacts(lang: str) -> str:
    lines = [TEXTS[lang]["contacts_title"], ""]
    for key, value in PROFILE["contacts"].items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def generate_password(length: int = 16) -> str:
    """Генерирует пароль с буквами разного регистра, цифрами и символами."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)
        ):
            return password


# ---------- Обработчики ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Срабатывает на команду /start."""
    await update.message.reply_text(
        t(context, "welcome").format(name=PROFILE["name"]),
        reply_markup=main_menu(context),
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Срабатывает при нажатии любой инлайн-кнопки."""
    query = update.callback_query
    await query.answer()
    action = query.data
    lang = get_lang(context)

    if action == "toggle_lang":
        # Переключаем язык и сохраняем его для этого пользователя
        context.user_data["lang"] = "ru" if lang == "en" else "en"
        lang = get_lang(context)
        await query.edit_message_text(TEXTS[lang]["menu"], reply_markup=main_menu(context))

    elif action == "menu":
        await query.edit_message_text(t(context, "menu"), reply_markup=main_menu(context))

    elif action == "about":
        await query.edit_message_text(PROFILE["about"][lang], reply_markup=back_button(context))

    elif action == "skills":
        await query.edit_message_text(format_skills(lang), reply_markup=back_button(context))

    elif action == "projects":
        await query.edit_message_text(format_projects(lang), reply_markup=back_button(context))

    elif action == "contacts":
        await query.edit_message_text(format_contacts(lang), reply_markup=back_button(context))

    elif action == "password":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(context, "again"), callback_data="password")],
            [InlineKeyboardButton(t(context, "back"), callback_data="menu")],
        ])
        await query.edit_message_text(
            f"{t(context, 'password_title')}\n\n{generate_password()}",
            reply_markup=keyboard,
        )


# ---------- Запуск ----------

def main() -> None:
    if not TOKEN:
        raise SystemExit("Токен не найден. Проверь файл .env (строка BOT_TOKEN=...).")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))

    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()