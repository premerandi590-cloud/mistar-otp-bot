import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

API_ID = 30956542
API_HASH = "b36f49d94e7bb1109e22d7ee405d41b6"
BOT_TOKEN = "8225731681:AAF_hcyuQze98XBdpQSjshqS-Z8EW5jnQmw"

ADMIN_ID = 8626918981

delete_time = 10
auto_delete_status = True
premium_users = []

app = Client(
    "AutoDeleteBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

menu = ReplyKeyboardMarkup(
    [
        ["⏱ Set Time", "⭐ Premium"],
        ["🗑 Delete Old Msg", "⚡ Auto Delete ON/OFF"],
        ["ℹ️ Help"]
    ],
    resize_keyboard=True
)

# Start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Welcome to Auto Delete Pro Bot\n\nUse menu buttons below.",
        reply_markup=menu
    )

# Help menu
@app.on_message(filters.regex("ℹ️ Help"))
async def help_menu(client, message):
    await message.reply(
        "📌 Commands:\n\n"
        "/settime 30 - Set delete time\n"
        "/premium USER_ID - Add premium user\n\n"
        "Buttons:\n"
        "⚡ Auto Delete ON/OFF\n"
        "🗑 Delete Old Msg"
    )

# Set delete time
@app.on_message(filters.command("settime"))
async def set_time(client, message):
    global delete_time

    if message.from_user.id != ADMIN_ID:
        return await message.reply("❌ Only admin can change time")

    try:
        delete_time = int(message.command[1])
        await message.reply(f"✅ Delete time set to {delete_time} seconds")
    except:
        await message.reply("Usage: /settime 30")

# Toggle auto delete
@app.on_message(filters.regex("⚡ Auto Delete ON/OFF"))
async def toggle_delete(client, message):
    global auto_delete_status

    if message.from_user.id != ADMIN_ID:
        return

    auto_delete_status = not auto_delete_status

    if auto_delete_status:
        await message.reply("✅ Auto Delete Enabled")
    else:
        await message.reply("❌ Auto Delete Disabled")

# Delete old messages
@app.on_message(filters.regex("🗑 Delete Old Msg"))
async def delete_old(client, message):

    if message.from_user.id != ADMIN_ID:
        return await message.reply("❌ Only admin can delete")

    chat_id = message.chat.id
    deleted = 0

    async for msg in client.get_chat_history(chat_id, limit=100):
        try:
            await msg.delete()
            deleted += 1
        except:
            pass

    await message.reply(f"🗑 Deleted {deleted} old messages")

# Add premium user
@app.on_message(filters.command("premium"))
async def add_premium(client, message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.command[1])
        premium_users.append(user_id)
        await message.reply("⭐ User added to premium")
    except:
        await message.reply("Usage: /premium USER_ID")

# Auto delete messages
@app.on_message(filters.group)
async def auto_delete(client, message):

    if not auto_delete_status:
        return

    await asyncio.sleep(delete_time)

    try:
        await message.delete()
    except:
        pass

print("Bot running...")
app.run()
