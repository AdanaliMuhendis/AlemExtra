from AlemMuzik import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ " **➠ İYİ GECELER.. 🌚** ",
           " **➠ SESSİZCE UYU… 🙊** ",
           " **➠ TELEFONUNU BIRAK VE UYU, YOKSA HAYALET GELECEK…👻** ",
           " **➠ GÜNDÜZ DE UYU GECE DE UYU TEMBEL… 🥲** ",
           " **➠ ANNE!  BAK ŞUNA, YORGANIN ALTINDA SEVGİLİSİ İLE KONUŞUYOR… 😜** ",
           " **➠ BABA!  BÜTÜN GECE KARDEŞİMİN TELEFON KONUŞMLARINA BAK…🤭** ",
           " **➠ ÜZEMEZ KİMSE SENİ... 🙂** ",
           " **➠ İYİ GECELER TATLI RÜYALAR KENDİNE İYİ BAK..? ✨** ",
           " **➠ ARTIK ÇOK GEÇ OLDU GİT UYU... 🌌** ",
           " **➠ ANNE! BAK ŞUNA SAAT 23:00 OLDU HALA UYUMUYOR, TELEFONLA OYNUYOR…🕦** ",
           " **➠ YARIN SABAH OKULA GİTMEK İSTEMİYOR MUSUN? HALA UYANIK MISIN?... 🏫** ",
           " **➠ BİRADERİM, İYİ GECELER..? 😊** ",
           " **➠ BU GÜN HAVA ÇOK SOĞUK, KENDİMİ RAHAT HİSSEDİYORUM VE HEMEN YATIYORUM… 🌼** ",
           " **➠  İYİ GECELER… 🌷** ",
           " **➠ HUZURLU UYUYACAĞIM… 🏵️** ",
           " **➠ MERHABA EFENDİM, İYİ GECELER… 🍃** ",
           " **➠ HEY? UNUTMA YILDIZLAR DA KAYAR BİR GÜN… ☃️** ",
           " **➠ İYİGECELER BEBEĞİM, SAAT ÇOK GEÇ OLDU... ⛄** ",
           " **➠ AĞLAYACAĞIM EFENDİM, YANİ AĞLAYARAK UYUYACAĞIM SENDE AĞLA… 😁** ",
           " **➠ BALIĞA BALIK DENİR, GÜLLER KIRMIZI, MENEKŞELER MOR, NEYSE İYİ GECELER BAYAN …🌄** ",
           " **➠ İYİ GECELER, GECEN GÜZEL OLSUN… 🤭** ",
           " **➠ GECE OLDU, GÜN BİTTİ, GÜNEŞİN YERİNİ AY ALDI...(seni alan olmadı hayırlı geceler) 😊** ",
           " **➠ TÜM HAYALLERİNİZ GERÇEK OLSUN… ❤️** ",
           " **➠ İYİ GECELER TATLI RÜYALAR OLSUN… 💚** ",
           " **➠ İYİ GECELER, ÇOK UYKUM VAR… 🥱** ",
           " **➠ GÜZEL ARKADAŞIM, İYİ GECELER… 💤** ",
           " **➠ GECENİN GEÇ SAATLERİNE KADAR UYANIK KALARAK NE YAPIYORSUN, UYUMAK İSTEMİYOR MUSUN… 😜** ",
           " **➠ GÖZLERİNİZİ KAPATIN, SIMSIKI SARILIN VE UNUTMAYIN Kİ GECE BOYUNCA MELEKLER SİZİ İZLEYECEK VE KORUYACAK... 💫** ",
        ]

VC_TAG = [ "**➠ GÜNAYDIN, NASILSIN?.. 🐱**",
         "**➠ GÜNAYDIN, SABAH OLDU KALKMAN GEREKMİYOR MU?.. 🌤️**",
         "**➠ GÜNAYDIN BEBEĞİM, ÇAY İÇ ALSANAĞĞĞ ☕**",
         "**➠ ERKEN KALK, OKULA\İŞE GİTMİYOR MUSUN?.. 🏫**",
         "**➠ GÜNAYDIN, SESSİZCE YATAKTAN KALK YOKSA SU DÖKECEĞİM… 🧊**",
         "**➠ BEBEĞİM UYAN VE TAZELEN, KAHVALTI HAZIR 🫕**",
         "**➠ NEDEN İŞE GİTMEK İSTEMİYORSUN BU GÜN… 🏣**",
         "**➠ GÜNAYDIN, NE İSTERSİN ÇAY\KAHVE… ☕🍵**",
         "**➠ BEBEĞİM SAAT 8 VE SEN HALA UYANMADIN MI? 🕖**",
         "**➠ GÜNAYDIN, GÜZEL BİR GÜN GEÇİRMENİZ DİLEĞİYLE... 🌄**",
         "**➠ GÜNAYDIN, İYİ BİR GÜN GEÇİRMENİZ DİLEĞİYLE... 🪴**",
         "**➠ GÜNAYDIN, NASILSIN BEBEĞİM… 😇**",
         "**➠ ANNE! BAK BU DEĞERSİZ İNSAN HALA UYUYOR... 😵‍💫**",
         "**➠ DOSTUM BÜTÜN GECE UYUYOR MUYDUN? HALA UYUYORSUN, KALKMAK İSTEMİYOR MUSUN 😏**",
         "**➠ ÇİÇEĞİM GÜNAYDIN, KALK VE GRUPTAKİ BÜTÜN ARKADAŞLARINA İYİ DİLEKLER SÖYLE 🌟**",
         "**➠ BABA! HALA UYANMADI, OKUL VAKTİ YAKLAŞIYOR... 🥲**",
         "**➠ GÜNAYDIN TATLIM, NE YAPIYORSUN... 😅**",
         "**➠ GÜNAYDIN, BENİM BEST FRİENDİMİN KAHVALTISI NEREDEĞĞĞ 🍳**",
        ]


@app.on_message(filters.command(["gntag", "gn", "goodnight" ], prefixes=["/", "@", "#", "Alem", "Alem"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ BU KOMUTLAR SADECE GRUP İÇERİSİNDE KULLANILABİLİR.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ YÖNETİCİ DEĞİLSİNİZ BEBEĞİM, SADECE YÖNETİCİLER ÜYELERİ ETİKETLEYEBİLİR. ")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall YAZDIKTAN SONRA MESAJINIZI YAZINIZ YADA MESAJINIZI YANITLAYARAK TAG YAPABİLİRSİNİZ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall YAZDIKTAN SONRA MESAJINIZI YAZINIZ YADA MESAJINIZI YANITLAYARAK TAG YAPABİLİRSİNİZ...")
    else:
        return await message.reply("/tagall YAZDIKTAN SONRA MESAJINIZI YAZINIZ YADA MESAJINIZI YANITLAYARAK TAG YAPABİLİRSİNİZ...")
    if chat_id in spam_chats:
        return await message.reply("๏ LÜTFEN İLK ÖNCE ÇALIŞAN İŞLEMİ DURDURUN...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["gmtag", "gm"], prefixes=["/", "@", "#", "Alem", "Alem"]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ YÖNETİCİ DEĞİLSİNİZ BEBEĞİM, SADECE YÖNETİCİLER ÜYELERİ ETİKETLEYEBİLİR. ")
    if chat_id in spam_chats:
        return await message.reply("๏ LÜTFEN İLK ÖNCE ÇALIŞAN İŞLEMİ DURDURUN...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@app.on_message(filters.command(["gmstop", "gnstop", "cancle"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ BU KOMUTLAR SADECE GRUP İÇERİSİNDE KULLANILABİLİR.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ YÖNETİCİ DEĞİLSİNİZ BEBEĞİM, SADECE YÖNETİCİLER ÜYELERİ ETİKETLEYEBİLİR.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ETİKETLEME SÜRECİ DURDURULDU ๏")

