from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import logging
import re

# Loglama yapılandırması
logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s', level=logging.INFO)

# Küfür listesini yükleme
with open('küfür.txt', 'r', encoding='utf-8') as f:
    küfür_listesi = [line.strip().lower() for line in f]

# Mesaj işleyici fonksiyon
async def mesaj_filtresi(update: Update, context: CallbackContext) -> None:
    mesaj = update.message.text
    mesaj_lower = mesaj.lower()
    kullanıcı = update.message.from_user.username
    
    # Küfür içeren kelime kontrolü ve sansürleme
    sansürlü_mesaj = mesaj
    for küfür in küfür_listesi:
        if küfür in mesaj_lower:
            # Küfürlü kelimeyi sansürle
            sansürlü_kelime = küfür[0] + '*' * (len(küfür) - 2) + küfür[-1]
            sansürlü_mesaj = re.sub(r'\b' + küfür + r'\b', sansürlü_kelime, sansürlü_mesaj, flags=re.IGNORECASE)
    
    # Eğer sansürleme yapılmışsa mesajı silip sansürlü mesajı gönder
    if sansürlü_mesaj != mesaj:
        await update.message.delete()
        bildirim = f"⚠️ @{kullanıcı} tarafından yazılan mesaj sansürlendi: \"{sansürlü_mesaj}\""
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bildirim)
        logging.info(f"Mesaj sansürlendi: \"{sansürlü_mesaj}\" kullanıcısı: @{kullanıcı}")

# Main fonksiyonu
def main() -> None:
    # Botunuzun tokeni
    token = ""
    app = Application.builder().token(token).build()

    # Mesajları işleyiciye yönlendirme
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_filtresi))

    # Botu çalıştırma
    app.run_polling()

if __name__ == '__main__':
    main()
