import random
import asyncio
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8572966464:AAGVOZgABxMg3boLEpmB3JyDtp-xG6hA3aM"

# 💥 FIX QUYỀN FILE → lưu ra Desktop
DATA_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "data.json")

# ================== LOAD & SAVE ==================
def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(users, f)
    except Exception as e:
        print("LOI SAVE:", e)

users = load_data()

# ================== LOGIC ==================
def xoc_dia():
    result = [random.randint(0,1) for _ in range(4)]
    red = sum(result)
    dice = "".join(["🔴" if x==1 else "⚪" for x in result])

    if red == 0:
        return f"{dice} → 4 trắng"
    elif red == 4:
        return f"{dice} → 4 đỏ"
    elif red == 2:
        return f"{dice} → chẵn"
    else:
        return f"{dice} → lẻ"

# ================== MENU ==================
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Chẵn 5000", callback_data="chan_5000"),
         InlineKeyboardButton("🎮 Lẻ 5000", callback_data="le_5000")],
        [InlineKeyboardButton("💰 Chẵn 50000", callback_data="chan_50000"),
         InlineKeyboardButton("💰 Lẻ 50000", callback_data="le_50000")]
    ])

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if user_id not in users:
        users[user_id] = 10000
        save_data()

    await update.message.reply_text(
        f"🎲 XÓC ĐĨA CASINO\n💰 {users[user_id]}",
        reply_markup=menu()
    )

# ================== BUTTON ==================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if user_id not in users:
        users[user_id] = 10000

    try:
        choice, money = query.data.split("_")
        money = int(money)
    except:
        await query.message.reply_text("❌ Lỗi dữ liệu")
        return

    if users[user_id] < money:
        await query.message.reply_text("❌ Không đủ tiền")
        return

    try:
        msg = await query.message.reply_text("🎥 Đang lắc bát...")

        await asyncio.sleep(2)
        await msg.edit_text("🔥 Lắc mạnh...")

        await asyncio.sleep(1)

        result = xoc_dia()

        if choice in result:
            users[user_id] += money
            text = f"💥 THẮNG +{money}\n👉 {result}\n💰 {users[user_id]}"
        else:
            users[user_id] -= money
            text = f"💀 THUA -{money}\n👉 {result}\n💰 {users[user_id]}"

        save_data()

        await msg.edit_text(text, reply_markup=menu())

    except Exception as e:
        print("LOI THAT:", e)
        await query.message.reply_text("❌ Lỗi rồi, xem CMD")

# ================== NẠP ==================
async def nap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if user_id not in users:
        users[user_id] = 10000

    try:
        amount = int(context.args[0])
    except:
        await update.message.reply_text("Dùng: /nap 1000")
        return

    users[user_id] += amount
    save_data()

    await update.message.reply_text(f"💎 +{amount}\n💰 {users[user_id]}")

# ================== MONEY ==================
async def money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    await update.message.reply_text(f"💰 {users.get(user_id,10000)}")

# ================== RUN ==================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nap", nap))
app.add_handler(CommandHandler("money", money))
app.add_handler(CallbackQueryHandler(button))

print("BOT DANG CHAY...")
app.run_polling()