from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters

TOKEN = "8188309515:AAGxQFJ6Resmrx-KV3yKJ7-iWX3-Pq9CYPU"
ADMINS = [5109569250]

akun_list = [
    {"id": 1, "hero": "Nana", "rank": "Epic", "harga": "Rp200.000"},
    {"id": 2, "hero": "Lancelot", "rank": "Mythic", "harga": "Rp350.000"},
]

def is_admin(user_id):
    return user_id in ADMINS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Selamat datang di Bot Jual Beli Akun ML!\nKetik /help untuk melihat semua perintah.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📋 Perintah yang tersedia:\n"
        "/list_akun - Lihat semua akun ML\n"
        "/detail <id> - Lihat detail akun\n"
        "/beli <id> - Beli akun ML\n"
        "/contact - Hubungi admin\n"
        "/tambah_akun <hero> <rank> <harga> - (Admin saja)\n"
    )
    await update.message.reply_text(text)

async def list_akun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not akun_list:
        return await update.message.reply_text("Belum ada akun tersedia.")
    text = "📦 Daftar Akun:\n"
    for akun in akun_list:
        text += f"ID {akun['id']}: {akun['hero']} - {akun['rank']} - {akun['harga']}\n"
    await update.message.reply_text(text)

async def detail_akun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("Gunakan: /detail <id>")
    try:
        akun_id = int(context.args[0])
        akun = next((a for a in akun_list if a['id'] == akun_id), None)
        if not akun:
            return await update.message.reply_text("Akun tidak ditemukan.")
        text = f"🔍 Detail Akun ID {akun['id']}:\nHero: {akun['hero']}\nRank: {akun['rank']}\nHarga: {akun['harga']}"
        keyboard = [[InlineKeyboardButton("🛒 Beli Sekarang", callback_data=f"beli_{akun_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text("ID harus berupa angka.")

async def beli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("Gunakan: /beli <id>")
    try:
        akun_id = int(context.args[0])
        akun = next((a for a in akun_list if a['id'] == akun_id), None)
        if not akun:
            return await update.message.reply_text("Akun tidak ditemukan.")
        await update.message.reply_text(f"✅ Pembelian akun {akun['hero']} berhasil diproses. Admin akan menghubungi Anda.")
    except ValueError:
        await update.message.reply_text("ID harus berupa angka.")

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Hubungi admin melalui Telegram: @cassynndr")

async def tombol_beli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("beli_"):
        akun_id = int(data.split("_")[1])
        akun = next((a for a in akun_list if a['id'] == akun_id), None)
        if akun:
            await query.edit_message_text(f"✅ Pembelian akun {akun['hero']} berhasil diproses. Admin akan menghubungi Anda.")

async def tambah_akun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return await update.message.reply_text("❌ Akses ditolak. Hanya admin yang dapat menambahkan akun.")
    if len(context.args) < 3:
        return await update.message.reply_text("Gunakan: /tambah_akun <hero> <rank> <harga>")
    hero = context.args[0]
    rank = context.args[1]
    harga = context.args[2]
    new_id = max([a['id'] for a in akun_list]) + 1 if akun_list else 1
    akun_list.append({"id": new_id, "hero": hero, "rank": rank, "harga": harga})
    await update.message.reply_text(f"✅ Akun baru berhasil ditambahkan dengan ID {new_id}.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Maaf, saya tidak mengerti. Ketik /help untuk melihat perintah.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list_akun", list_akun))
    app.add_handler(CommandHandler("detail", detail_akun))
    app.add_handler(CommandHandler("beli", beli))
    app.add_handler(CommandHandler("contact", contact_admin))
    app.add_handler(CommandHandler("tambah_akun", tambah_akun))
    app.add_handler(CallbackQueryHandler(tombol_beli))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    print("✅ Bot aktif...")
    app.run_polling()

if __name__ == "__main__":
    main()
