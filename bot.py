import random
import asyncio
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Lấy Token từ biến môi trường để bảo mật, nếu không có sẽ dùng mặc định
TOKEN = os.getenv("TELEGRAM_TOKEN", "8572966464:AAGVOZgABxMg3boLEpmB3JyDtp-xG6hA3aM")

# FIX: Chỉ lưu file data.json ở thư mục hiện tại (Server không có thư mục Desktop)
DATA_FILE = "data.json"

# ================== LOAD & SAVE ==================
def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi Load Data: {e}")
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi Save Data: {e}")

# Khởi tạo dữ liệu từ file
users = load_data()

# ================== LOGIC GAME ==================
def xoc_dia():
    result = [random.randint(0,1) for _ in range(4)]
    red = sum(result)
    dice = "".join(["🔴" if x==1 else "⚪" for x in result])

    if red == 0: return f"{dice} → 4 trắng (Chẵn)"
    elif red == 4: return f"{dice} → 4 đỏ (Chẵn)"
    elif red == 2: return f"{dice} → 2 đỏ 2 trắng (Chẵn)"
    else: return f"{dice} → lẻ"

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Chẵn 5k", callback_data="chan_5000"),
         InlineKeyboardButton("🎮 Lẻ 5k", callback_data="le_5000")],
        [InlineKeyboardButton("💰 Chẵn 50k", callback_data="chan_50000"),
         InlineKeyboardButton("💰 Lẻ 50k", callback_data="le_50000")]
    ])

# ================== HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        users[user_id] = 10000
        save_data(users)

    await update.message.reply_text(
        f"🎲 XÓC ĐĨA CASINO\n💰 Số dư: {users[user_id]:,} VNĐ",
        reply_markup=menu()
    )

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
        return

    if users[user_id] < money:
        await query.message.reply_text("❌ Bạn không đủ tiền để cược!")
        return

    msg = await query.edit_message_text("🎥 Đang xóc bát...")
    await asyncio.sleep(1.5)
    
    result_str = xoc_dia()
    is_win = False
    
    # Kiểm tra thắng thua
    if choice == "chan" and "Chẵn" in result_str: is_win = True
    if choice == "le" and "lẻ" in result_str: is_win = True

    if is_win:
        users[user_id] += money
        text = f"💥 THẮNG +{money:,}\n👉 Kết quả: {result_str}\n💰 Số dư: {users[user_id]:,}"
    else:
        users[user_id] -= money
        text = f"💀 THUA -{money:,}\n👉 Kết quả: {result_str}\n💰 Số dư: {users[user_id]:,}"

    save_data(users)
    await msg.edit_text(text, reply_markup=menu())

async def nap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    try:
        amount = int(context.args[0])
        users[user_id] = users.get(user_id, 10000) + amount
        save_data(users)
        await update.message.reply_text(f"✅ Đã nạp {amount:,}\n💰 Tổng dư: {users[user_id]:,}")
    except:
        await update.message.reply_text("Cú pháp: `/nap 50000`", parse_mode="Markdown")

# ================== RUN ==================
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nap", nap))
    app.add_handler(CallbackQueryHandler(button))

    print("--- BOT XÓC ĐĨA ĐANG ONLINE ---")
    app.run_polling()
