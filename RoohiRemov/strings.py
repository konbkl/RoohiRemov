"""Texts, fonts, blockquotes. English default; baaki sab languages me full translation.
Missing key => English fallback. Line ke aage '~' lagao to us line pe font nahi lagega."""
import html, re

LANGS = {"en": "English", "hg": "Hinglish", "hi": "Hindi", "my": "Burmese", "uz": "Uzbek",
         "ru": "Russian", "ar": "Arabic", "es": "Spanish", "fr": "French", "bn": "Bengali"}
FLAGS = {"en": "🇬🇧", "hg": "🇮🇳", "hi": "🇮🇳", "my": "🇲🇲", "uz": "🇺🇿", "ru": "🇷🇺",
         "ar": "🌐", "es": "🌐", "fr": "🌐", "bn": "🌐"}

# ---------- font (screenshot style: Λ ε σ η) — mapping yahin edit kar sakte ho ----------
_MAP = dict(zip("abcdefghijklmnopqrstuvwxyz", "Λʙᴄᴅεꜰɢʜɪᴊᴋʟᴍησᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"))
_FONT = str.maketrans({**_MAP, **{k.upper(): v for k, v in _MAP.items()}})
_KEEP = re.compile(r"(<b>.*?</b>|<a .*?</a>|<tg-emoji.*?</tg-emoji>|<[^>]+>|&\w+;|(?<!\S)/[A-Za-z_]+)", re.S)

def sc(text: str) -> str:
    parts = _KEEP.split(text)
    return "".join(p if i % 2 else p.translate(_FONT) for i, p in enumerate(parts))

BUTTONS = {"t_users","t_bots","t_channels","t_captions","t_usernames","t_admins","home","close","back",
           "add","helpcmd","updates","support","chlang"}          # font, par blockquote nahi
NOQUOTE = BUTTONS | {"welcome", "lang_set"}                          # welcome me quotes already hain
EXPAND = {"help", "live"}                                            # expandable blockquote
DIV = "•──────────────────────────•"

S = {}
S["en"] = {
 "welcome": "<blockquote>Salutations {name},</blockquote>\n<blockquote expandable>✧ Welcome to {bot} — a powerful & fast link protection bot\n✧ Built for clean • safe • spam-free groups\n✧ Auto-deletes links, invite links, channel promos & unwanted usernames\n✧ Add me to a group and give <b>Delete Messages</b> permission\n" + DIV + "\n✧ Use help to view all commands and features</blockquote>",
 "groups_only": "{warn} /settings works in <b>groups only</b>.\n~\n~Add me to your group and use it there.\n~Send /help to see available commands.",
 "no_perm": "{cross} You are not allowed to do this.",
 "settings": "{gear} LINK POLICY PANEL\n\nTap to toggle. {tick} = blocked, {cross} = allowed.\nApproved users: {au} · Whitelisted links: {wl} · Blacklisted words: {bl}",
 "lang_pick": "{globe} CHOOSE THIS GROUP'S LANGUAGE",
 "lang_set": "Language updated.",
 "deleted": "{ban} {user}, links are not allowed here.",
 "deleted_bl": "{ban} {user}, that word/phrase is blacklisted.",
 "need_admin": "{warn} Make me admin with <b>Delete Messages</b> permission, otherwise I can't remove links.",
 "help": "{gear} CONTROL CENTER\n\n{help} ESSENTIAL COMMANDS\n/settings — open link policy panel\n/language — change group language\n/allowed — show approved users\n/whitelist — show allowed links\n\n{crown} USER MANAGEMENT\n/allow — approve a user\n/disallow — remove approval\n/whitelist &lt;url&gt; — allow a specific link (max 10)\n/rwhitelist &lt;url&gt; — remove from whitelist\n\n{ban} SMART BLACKLIST\n/blacklist &lt;text&gt; — blacklist a word/phrase (or reply)\n/rblacklist &lt;n|text&gt; — remove from blacklist\n/blacklisted — list all blacklisted words\n\n{user} Group owners can allow or block admins from editing bot settings.",
 "live": "{rocket} ROOHIREMOV IS NOW LIVE!\n\nA smart and fast group protection bot made to keep your chats clean and safe.\n\n{diamond} No user can send links\n{diamond} No bot can send links\n{diamond} Deletes external links automatically\n{diamond} Supports user, bot, channel and caption link filtering\n{diamond} Group owner can control the rules\n{diamond} Approved users can be allowed with /allow\n\nAdd me to your group and keep link spam away.",
 "need_target": "Reply to a user or send a user ID.",
 "allowed_ok": "{tick} {user} approved.", "allowed_dup": "Already approved.",
 "disallowed": "{tick} Approval removed.", "not_found": "Not found.",
 "allowed_list": "{user} APPROVED USERS\n{items}", "empty": "— empty —",
 "wl_list": "{shield} ALLOWED LINKS\n{items}", "wl_ok": "{tick} Whitelisted.", "wl_max": "{warn} Max 10 links.",
 "wl_usage": "Usage: /whitelist &lt;url&gt;", "wl_rm": "{tick} Removed from whitelist.",
 "bl_ok": "{tick} Blacklisted.", "bl_rm": "{tick} Removed from blacklist.",
 "bl_list": "{ban} BLACKLISTED WORDS\n{items}", "bl_usage": "Usage: /blacklist &lt;text&gt; or reply to a message.",
 "t_users": "Users", "t_bots": "Bots", "t_channels": "Channels", "t_captions": "Captions",
 "t_usernames": "@Usernames", "t_admins": "Admins can edit", "home": "Home", "close": "Close", "back": "Back",
 "add": "✧₊ Add me to your chat ₊✧", "helpcmd": "Help & Commands", "updates": "Updates", "support": "Support", "chlang": "Change Language",
}
S["hg"] = {
 "welcome": "<blockquote>Namaste {name},</blockquote>\n<blockquote expandable>✧ {bot} me aapka swagat hai — ek powerful aur fast link protection bot\n✧ Clean • safe • spam-free groups ke liye bana hai\n✧ Links, invite links, channel promos aur unwanted usernames auto-delete karta hai\n✧ Mujhe group me add karo aur <b>Delete Messages</b> permission do\n" + DIV + "\n✧ Saare commands aur features dekhne ke liye help use karo</blockquote>",
 "groups_only": "{warn} /settings <b>sirf groups me</b> kaam karta hai.\n~\n~Mujhe apne group me add karo aur wahin use karo.\n~Saare commands dekhne ke liye /help bhejo.",
 "no_perm": "{cross} Aapko ye karne ki permission nahi hai.",
 "settings": "{gear} LINK POLICY PANEL\n\nToggle karne ke liye tap karo. {tick} = block, {cross} = allowed.\nApproved users: {au} · Whitelist links: {wl} · Blacklist words: {bl}",
 "lang_pick": "{globe} IS GROUP KI LANGUAGE CHUNO",
 "lang_set": "Language badal di gayi.",
 "deleted": "{ban} {user}, yahan links bhejna mana hai.",
 "deleted_bl": "{ban} {user}, ye word/phrase blacklist me hai.",
 "need_admin": "{warn} Mujhe admin banao aur <b>Delete Messages</b> permission do, tabhi main links hata paunga.",
 "help": "{gear} CONTROL CENTER\n\n{help} ZAROORI COMMANDS\n/settings — link policy panel kholo\n/language — group ki language badlo\n/allowed — approved users dekho\n/whitelist — allowed links dekho\n\n{crown} USER MANAGEMENT\n/allow — user ko approve karo\n/disallow — approval hatao\n/whitelist &lt;url&gt; — koi specific link allow karo (max 10)\n/rwhitelist &lt;url&gt; — whitelist se hatao\n\n{ban} SMART BLACKLIST\n/blacklist &lt;text&gt; — word/phrase blacklist karo (ya reply)\n/rblacklist &lt;n|text&gt; — blacklist se hatao\n/blacklisted — saare blacklisted words dekho\n\n{user} Group owner chahe to admins ko bot settings edit karne se rok sakta hai.",
 "live": "{rocket} ROOHIREMOV AB LIVE HAI!\n\nEk smart aur fast group protection bot jo aapki chats ko clean aur safe rakhta hai.\n\n{diamond} Koi user link nahi bhej sakta\n{diamond} Koi bot link nahi bhej sakta\n{diamond} External links apne aap delete\n{diamond} User, bot, channel aur caption link filter\n{diamond} Group owner rules control karta hai\n{diamond} Approved users ko /allow se allow karo\n\nMujhe apne group me add karo aur link spam door rakho.",
 "need_target": "Kisi user ko reply karo ya user ID bhejo.",
 "allowed_ok": "{tick} {user} approve ho gaya.", "allowed_dup": "Pehle se approved hai.",
 "disallowed": "{tick} Approval hata diya.", "not_found": "Nahi mila.",
 "allowed_list": "{user} APPROVED USERS\n{items}", "empty": "— khali —",
 "wl_list": "{shield} ALLOWED LINKS\n{items}", "wl_ok": "{tick} Whitelist me add ho gaya.", "wl_max": "{warn} Max 10 links hi allowed hain.",
 "wl_usage": "Use karo: /whitelist &lt;url&gt;", "wl_rm": "{tick} Whitelist se hata diya.",
 "bl_ok": "{tick} Blacklist me add ho gaya.", "bl_rm": "{tick} Blacklist se hata diya.",
 "bl_list": "{ban} BLACKLISTED WORDS\n{items}", "bl_usage": "Use karo: /blacklist &lt;text&gt; ya kisi message ko reply karo.",
 "t_users": "Users", "t_bots": "Bots", "t_channels": "Channels", "t_captions": "Captions",
 "t_usernames": "@Usernames", "t_admins": "Admins edit kar sakte", "home": "Home", "close": "Close", "back": "Back",
 "add": "✧₊ Mujhe apne chat me add karo ₊✧", "helpcmd": "Help & Commands", "updates": "Updates", "support": "Support", "chlang": "Language badlo",
}
S["hi"] = {
 "welcome": "<blockquote>नमस्ते {name},</blockquote>\n<blockquote expandable>✧ {bot} में आपका स्वागत है — एक पावरफुल और फास्ट लिंक प्रोटेक्शन बॉट\n✧ साफ • सुरक्षित • स्पैम-फ्री ग्रुप के लिए बना है\n✧ लिंक, इनवाइट लिंक, चैनल प्रमोशन और अनचाहे यूज़रनेम अपने-आप डिलीट करता है\n✧ मुझे ग्रुप में जोड़ें और <b>Delete Messages</b> परमिशन दें\n" + DIV + "\n✧ सभी कमांड और फीचर देखने के लिए हेल्प दबाएँ</blockquote>",
 "groups_only": "{warn} /settings सिर्फ <b>ग्रुप</b> में काम करता है।\n~\n~मुझे अपने ग्रुप में जोड़ें और वहीं इस्तेमाल करें।\n~कमांड देखने के लिए /help भेजें।",
 "no_perm": "{cross} आपको यह करने की अनुमति नहीं है।",
 "settings": "{gear} लिंक पॉलिसी पैनल\n\nबदलने के लिए टैप करें। {tick} = ब्लॉक, {cross} = अनुमति।\nअप्रूव्ड यूज़र: {au} · व्हाइटलिस्ट लिंक: {wl} · ब्लैकलिस्ट शब्द: {bl}",
 "lang_pick": "{globe} इस ग्रुप की भाषा चुनें",
 "lang_set": "भाषा बदल दी गई।",
 "deleted": "{ban} {user}, यहाँ लिंक भेजना मना है।",
 "deleted_bl": "{ban} {user}, यह शब्द/वाक्य ब्लैकलिस्ट में है।",
 "need_admin": "{warn} मुझे <b>Delete Messages</b> परमिशन के साथ एडमिन बनाएँ, वरना मैं लिंक नहीं हटा पाऊँगा।",
 "help": "{gear} कंट्रोल सेंटर\n\n{help} ज़रूरी कमांड\n/settings — लिंक पॉलिसी पैनल खोलें\n/language — ग्रुप की भाषा बदलें\n/allowed — अप्रूव्ड यूज़र देखें\n/whitelist — अनुमति वाले लिंक देखें\n\n{crown} यूज़र मैनेजमेंट\n/allow — यूज़र को अप्रूव करें\n/disallow — अप्रूवल हटाएँ\n/whitelist &lt;url&gt; — कोई लिंक अनुमति दें (अधिकतम 10)\n/rwhitelist &lt;url&gt; — व्हाइटलिस्ट से हटाएँ\n\n{ban} स्मार्ट ब्लैकलिस्ट\n/blacklist &lt;text&gt; — शब्द/वाक्य ब्लैकलिस्ट करें (या रिप्लाई)\n/rblacklist &lt;n|text&gt; — ब्लैकलिस्ट से हटाएँ\n/blacklisted — सभी ब्लैकलिस्ट शब्द देखें\n\n{user} ग्रुप ओनर चाहे तो एडमिन को बॉट सेटिंग बदलने से रोक सकता है।",
 "live": "{rocket} रूही रिमूव अब लाइव है!\n\nएक स्मार्ट और फास्ट ग्रुप प्रोटेक्शन बॉट जो आपकी चैट को साफ और सुरक्षित रखता है।\n\n{diamond} कोई यूज़र लिंक नहीं भेज सकता\n{diamond} कोई बॉट लिंक नहीं भेज सकता\n{diamond} बाहरी लिंक अपने-आप डिलीट\n{diamond} यूज़र, बॉट, चैनल और कैप्शन लिंक फ़िल्टर\n{diamond} ग्रुप ओनर नियम कंट्रोल करता है\n{diamond} /allow से अप्रूव्ड यूज़र को अनुमति दें\n\nमुझे अपने ग्रुप में जोड़ें और लिंक स्पैम से बचें।",
 "need_target": "किसी यूज़र को रिप्लाई करें या यूज़र ID भेजें।",
 "allowed_ok": "{tick} {user} अप्रूव हो गया।", "allowed_dup": "पहले से अप्रूव्ड है।",
 "disallowed": "{tick} अप्रूवल हटा दिया।", "not_found": "नहीं मिला।",
 "allowed_list": "{user} अप्रूव्ड यूज़र\n{items}", "empty": "— खाली —",
 "wl_list": "{shield} अनुमति वाले लिंक\n{items}", "wl_ok": "{tick} व्हाइटलिस्ट में जुड़ गया।", "wl_max": "{warn} अधिकतम 10 लिंक।",
 "wl_usage": "उपयोग: /whitelist &lt;url&gt;", "wl_rm": "{tick} व्हाइटलिस्ट से हटा दिया।",
 "bl_ok": "{tick} ब्लैकलिस्ट में जुड़ गया।", "bl_rm": "{tick} ब्लैकलिस्ट से हटा दिया।",
 "bl_list": "{ban} ब्लैकलिस्ट शब्द\n{items}", "bl_usage": "उपयोग: /blacklist &lt;text&gt; या किसी मैसेज को रिप्लाई करें।",
 "t_users": "यूज़र", "t_bots": "बॉट", "t_channels": "चैनल", "t_captions": "कैप्शन",
 "t_usernames": "@यूज़रनेम", "t_admins": "एडमिन एडिट कर सकें", "home": "होम", "close": "बंद करें", "back": "वापस",
 "add": "✧₊ मुझे अपनी चैट में जोड़ें ₊✧", "helpcmd": "हेल्प और कमांड", "updates": "अपडेट्स", "support": "सपोर्ट", "chlang": "भाषा बदलें",
}
S["my"] = {
 "welcome": "<blockquote>မင်္ဂလာပါ {name},</blockquote>\n<blockquote expandable>✧ {bot} မှ ကြိုဆိုပါတယ် — အားကောင်းပြီး မြန်ဆန်သော လင့်ခ်ကာကွယ်ရေး ဘော့တ်\n✧ သန့်ရှင်း • လုံခြုံ • စပမ်းကင်းသော အုပ်စုများအတွက် ဖန်တီးထားသည်\n✧ လင့်ခ်များ၊ ဖိတ်ကြားလင့်ခ်များ၊ ချန်နယ်ကြော်ငြာများနှင့် မလိုလားသော ယူဇာနိမ်းများကို အလိုအလျောက် ဖျက်ပေးသည်\n✧ ကျွန်ုပ်ကို အုပ်စုထဲထည့်ပြီး <b>Delete Messages</b> ခွင့်ပြုချက်ပေးပါ\n" + DIV + "\n✧ အမိန့်များနှင့် လုပ်ဆောင်ချက်အားလုံးကြည့်ရန် အကူအညီကိုနှိပ်ပါ</blockquote>",
 "groups_only": "{warn} /settings သည် <b>အုပ်စုများတွင်သာ</b> အလုပ်လုပ်သည်။\n~\n~ကျွန်ုပ်ကို သင့်အုပ်စုထဲထည့်ပြီး ထိုနေရာတွင် သုံးပါ။\n~အမိန့်များကြည့်ရန် /help ပို့ပါ။",
 "no_perm": "{cross} သင့်ကို ဤလုပ်ဆောင်ချက် ခွင့်မပြုပါ။",
 "settings": "{gear} လင့်ခ်မူဝါဒ ပင်နယ်\n\nပြောင်းရန် နှိပ်ပါ။ {tick} = ပိတ်ဆို့, {cross} = ခွင့်ပြု။\nခွင့်ပြုထားသူများ: {au} · ခွင့်ပြုလင့်ခ်များ: {wl} · ပိတ်ထားသောစကားလုံးများ: {bl}",
 "lang_pick": "{globe} ဤအုပ်စု၏ ဘာသာစကားကို ရွေးပါ",
 "lang_set": "ဘာသာစကား ပြောင်းပြီးပါပြီ။",
 "deleted": "{ban} {user}၊ ဤနေရာတွင် လင့်ခ်ပို့ခွင့်မရှိပါ။",
 "deleted_bl": "{ban} {user}၊ ထိုစကားလုံးသည် ပိတ်ထားသောစာရင်းတွင်ရှိသည်။",
 "need_admin": "{warn} <b>Delete Messages</b> ခွင့်ပြုချက်ဖြင့် ကျွန်ုပ်ကို admin လုပ်ပေးပါ၊ မဟုတ်ပါက လင့်ခ်များကို ဖယ်ရှားမရပါ။",
 "help": "{gear} ထိန်းချုပ်ရေးစင်တာ\n\n{help} အခြေခံအမိန့်များ\n/settings — လင့်ခ်မူဝါဒ ပင်နယ်ဖွင့်ရန်\n/language — အုပ်စုဘာသာစကားပြောင်းရန်\n/allowed — ခွင့်ပြုထားသူများကြည့်ရန်\n/whitelist — ခွင့်ပြုလင့်ခ်များကြည့်ရန်\n\n{crown} အသုံးပြုသူ စီမံခန့်ခွဲမှု\n/allow — အသုံးပြုသူကို ခွင့်ပြုရန်\n/disallow — ခွင့်ပြုချက်ဖယ်ရန်\n/whitelist &lt;url&gt; — လင့်ခ်တစ်ခုခွင့်ပြုရန် (အများဆုံး 10)\n/rwhitelist &lt;url&gt; — whitelist မှဖယ်ရန်\n\n{ban} စမတ် blacklist\n/blacklist &lt;text&gt; — စကားလုံး blacklist လုပ်ရန် (သို့ reply)\n/rblacklist &lt;n|text&gt; — blacklist မှဖယ်ရန်\n/blacklisted — blacklist စကားလုံးအားလုံးကြည့်ရန်\n\n{user} အုပ်စုပိုင်ရှင်သည် admin များ ဘော့တ်ဆက်တင်ပြင်ခွင့်ကို ခွင့်ပြု/ပိတ်နိုင်သည်။",
 "live": "{rocket} ROOHIREMOV ယခု အသက်ဝင်ပါပြီ!\n\nသင့်ချက်တ်များကို သန့်ရှင်းလုံခြုံစေသော စမတ်ကျပြီး မြန်ဆန်သည့် အုပ်စုကာကွယ်ရေးဘော့တ်။\n\n{diamond} အသုံးပြုသူများ လင့်ခ်မပို့နိုင်ပါ\n{diamond} ဘော့တ်များ လင့်ခ်မပို့နိုင်ပါ\n{diamond} ပြင်ပလင့်ခ်များကို အလိုအလျောက်ဖျက်သည်\n{diamond} အသုံးပြုသူ၊ ဘော့တ်၊ ချန်နယ်နှင့် caption လင့်ခ် စစ်ထုတ်သည်\n{diamond} အုပ်စုပိုင်ရှင်က စည်းမျဉ်းထိန်းချုပ်နိုင်သည်\n{diamond} /allow ဖြင့် ခွင့်ပြုနိုင်သည်\n\nကျွန်ုပ်ကို သင့်အုပ်စုထဲထည့်ပြီး လင့်ခ်စပမ်းကို ကာကွယ်ပါ။",
 "need_target": "အသုံးပြုသူကို reply လုပ်ပါ သို့မဟုတ် user ID ပို့ပါ။",
 "allowed_ok": "{tick} {user} ကို ခွင့်ပြုပြီးပါပြီ။", "allowed_dup": "ခွင့်ပြုပြီးသားဖြစ်သည်။",
 "disallowed": "{tick} ခွင့်ပြုချက် ဖယ်ရှားပြီးပါပြီ။", "not_found": "မတွေ့ပါ။",
 "allowed_list": "{user} ခွင့်ပြုထားသူများ\n{items}", "empty": "— ဗလာ —",
 "wl_list": "{shield} ခွင့်ပြုလင့်ခ်များ\n{items}", "wl_ok": "{tick} whitelist ထဲထည့်ပြီးပါပြီ။", "wl_max": "{warn} လင့်ခ် 10 ခုသာ။",
 "wl_usage": "အသုံးပြုပုံ: /whitelist &lt;url&gt;", "wl_rm": "{tick} whitelist မှဖယ်ပြီးပါပြီ။",
 "bl_ok": "{tick} blacklist ထဲထည့်ပြီးပါပြီ။", "bl_rm": "{tick} blacklist မှဖယ်ပြီးပါပြီ။",
 "bl_list": "{ban} ပိတ်ထားသောစကားလုံးများ\n{items}", "bl_usage": "အသုံးပြုပုံ: /blacklist &lt;text&gt; သို့မဟုတ် မက်ဆေ့ချ်ကို reply လုပ်ပါ။",
 "t_users": "အသုံးပြုသူ", "t_bots": "ဘော့တ်", "t_channels": "ချန်နယ်", "t_captions": "Caption",
 "t_usernames": "@ယူဇာနိမ်း", "t_admins": "Admin ပြင်နိုင်", "home": "ပင်မ", "close": "ပိတ်ရန်", "back": "နောက်သို့",
 "add": "✧₊ ကျွန်ုပ်ကို သင့်ချက်တ်ထဲထည့်ပါ ₊✧", "helpcmd": "အကူအညီ & အမိန့်များ", "updates": "အပ်ဒိတ်", "support": "အကူအညီ", "chlang": "ဘာသာစကားပြောင်း",
}
S["uz"] = {
 "welcome": "<blockquote>Assalomu alaykum {name},</blockquote>\n<blockquote expandable>✧ {bot} ga xush kelibsiz — kuchli va tezkor havola himoya boti\n✧ Toza • xavfsiz • spamsiz guruhlar uchun yaratilgan\n✧ Havolalar, taklif havolalari, kanal reklamalari va keraksiz usernamelarni avtomatik o'chiradi\n✧ Meni guruhga qo'shing va <b>Delete Messages</b> ruxsatini bering\n" + DIV + "\n✧ Barcha buyruqlar va imkoniyatlarni ko'rish uchun yordamni bosing</blockquote>",
 "groups_only": "{warn} /settings faqat <b>guruhlarda</b> ishlaydi.\n~\n~Meni guruhingizga qo'shing va o'sha yerda ishlating.\n~Buyruqlarni ko'rish uchun /help yuboring.",
 "no_perm": "{cross} Sizga bunga ruxsat yo'q.",
 "settings": "{gear} HAVOLA SIYOSATI PANELI\n\nO'zgartirish uchun bosing. {tick} = bloklangan, {cross} = ruxsat.\nTasdiqlangan: {au} · Oq ro'yxat havolalari: {wl} · Qora ro'yxat so'zlari: {bl}",
 "lang_pick": "{globe} BU GURUH TILINI TANLANG",
 "lang_set": "Til yangilandi.",
 "deleted": "{ban} {user}, bu yerda havola yuborish mumkin emas.",
 "deleted_bl": "{ban} {user}, bu so'z/ibora qora ro'yxatda.",
 "need_admin": "{warn} Meni <b>Delete Messages</b> ruxsati bilan admin qiling, aks holda havolalarni o'chira olmayman.",
 "help": "{gear} BOSHQARUV MARKAZI\n\n{help} ASOSIY BUYRUQLAR\n/settings — havola siyosati panelini ochish\n/language — guruh tilini o'zgartirish\n/allowed — tasdiqlanganlarni ko'rish\n/whitelist — ruxsat etilgan havolalar\n\n{crown} FOYDALANUVCHILARNI BOSHQARISH\n/allow — foydalanuvchini tasdiqlash\n/disallow — tasdiqni olib tashlash\n/whitelist &lt;url&gt; — havolaga ruxsat (maks. 10)\n/rwhitelist &lt;url&gt; — oq ro'yxatdan olib tashlash\n\n{ban} AQLLI QORA RO'YXAT\n/blacklist &lt;text&gt; — so'z/iborani bloklash (yoki reply)\n/rblacklist &lt;n|text&gt; — qora ro'yxatdan olib tashlash\n/blacklisted — barcha bloklangan so'zlar\n\n{user} Guruh egasi adminlarga bot sozlamalarini o'zgartirishga ruxsat berishi yoki taqiqlashi mumkin.",
 "live": "{rocket} ROOHIREMOV ENDI ISHDA!\n\nChatlaringizni toza va xavfsiz saqlovchi aqlli va tezkor guruh himoya boti.\n\n{diamond} Hech bir foydalanuvchi havola yubora olmaydi\n{diamond} Hech bir bot havola yubora olmaydi\n{diamond} Tashqi havolalar avtomatik o'chiriladi\n{diamond} Foydalanuvchi, bot, kanal va izoh havolalarini filtrlaydi\n{diamond} Guruh egasi qoidalarni boshqaradi\n{diamond} /allow orqali tasdiqlash mumkin\n\nMeni guruhingizga qo'shing va havola spamidan qutiling.",
 "need_target": "Foydalanuvchiga reply qiling yoki user ID yuboring.",
 "allowed_ok": "{tick} {user} tasdiqlandi.", "allowed_dup": "Allaqachon tasdiqlangan.",
 "disallowed": "{tick} Tasdiq olib tashlandi.", "not_found": "Topilmadi.",
 "allowed_list": "{user} TASDIQLANGANLAR\n{items}", "empty": "— bo'sh —",
 "wl_list": "{shield} RUXSAT ETILGAN HAVOLALAR\n{items}", "wl_ok": "{tick} Oq ro'yxatga qo'shildi.", "wl_max": "{warn} Maksimum 10 ta havola.",
 "wl_usage": "Foydalanish: /whitelist &lt;url&gt;", "wl_rm": "{tick} Oq ro'yxatdan olib tashlandi.",
 "bl_ok": "{tick} Qora ro'yxatga qo'shildi.", "bl_rm": "{tick} Qora ro'yxatdan olib tashlandi.",
 "bl_list": "{ban} BLOKLANGAN SO'ZLAR\n{items}", "bl_usage": "Foydalanish: /blacklist &lt;text&gt; yoki xabarga reply qiling.",
 "t_users": "Foydalanuvchilar", "t_bots": "Botlar", "t_channels": "Kanallar", "t_captions": "Izohlar",
 "t_usernames": "@Usernamelar", "t_admins": "Adminlar tahrirlay oladi", "home": "Bosh sahifa", "close": "Yopish", "back": "Orqaga",
 "add": "✧₊ Meni chatingizga qo'shing ₊✧", "helpcmd": "Yordam & Buyruqlar", "updates": "Yangiliklar", "support": "Qo'llab-quvvatlash", "chlang": "Tilni o'zgartirish",
}
S["ru"] = {
 "welcome": "<blockquote>Приветствую, {name},</blockquote>\n<blockquote expandable>✧ Добро пожаловать в {bot} — мощный и быстрый бот защиты от ссылок\n✧ Создан для чистых • безопасных • спам-свободных групп\n✧ Автоматически удаляет ссылки, инвайты, рекламу каналов и ненужные юзернеймы\n✧ Добавьте меня в группу и выдайте право <b>Delete Messages</b>\n" + DIV + "\n✧ Нажмите «Помощь», чтобы увидеть все команды и функции</blockquote>",
 "groups_only": "{warn} /settings работает <b>только в группах</b>.\n~\n~Добавьте меня в группу и используйте там.\n~Отправьте /help, чтобы увидеть команды.",
 "no_perm": "{cross} У вас нет прав на это действие.",
 "settings": "{gear} ПАНЕЛЬ ПОЛИТИКИ ССЫЛОК\n\nНажмите для переключения. {tick} = блок, {cross} = разрешено.\nОдобренные: {au} · Белый список: {wl} · Чёрный список: {bl}",
 "lang_pick": "{globe} ВЫБЕРИТЕ ЯЗЫК ГРУППЫ",
 "lang_set": "Язык обновлён.",
 "deleted": "{ban} {user}, ссылки здесь запрещены.",
 "deleted_bl": "{ban} {user}, это слово/фраза в чёрном списке.",
 "need_admin": "{warn} Сделайте меня админом с правом <b>Delete Messages</b>, иначе я не смогу удалять ссылки.",
 "help": "{gear} ЦЕНТР УПРАВЛЕНИЯ\n\n{help} ОСНОВНЫЕ КОМАНДЫ\n/settings — открыть панель политики ссылок\n/language — сменить язык группы\n/allowed — список одобренных\n/whitelist — разрешённые ссылки\n\n{crown} УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ\n/allow — одобрить пользователя\n/disallow — снять одобрение\n/whitelist &lt;url&gt; — разрешить ссылку (макс. 10)\n/rwhitelist &lt;url&gt; — убрать из белого списка\n\n{ban} УМНЫЙ ЧЁРНЫЙ СПИСОК\n/blacklist &lt;text&gt; — добавить слово/фразу (или ответом)\n/rblacklist &lt;n|text&gt; — убрать из чёрного списка\n/blacklisted — все запрещённые слова\n\n{user} Владелец группы может разрешить или запретить админам менять настройки бота.",
 "live": "{rocket} ROOHIREMOV ТЕПЕРЬ В СЕТИ!\n\nУмный и быстрый бот защиты групп, который держит ваши чаты чистыми и безопасными.\n\n{diamond} Пользователи не могут отправлять ссылки\n{diamond} Боты не могут отправлять ссылки\n{diamond} Внешние ссылки удаляются автоматически\n{diamond} Фильтрует ссылки от пользователей, ботов, каналов и в подписях\n{diamond} Владелец группы управляет правилами\n{diamond} Одобренным можно разрешить через /allow\n\nДобавьте меня в группу и забудьте про спам ссылками.",
 "need_target": "Ответьте на сообщение пользователя или отправьте его ID.",
 "allowed_ok": "{tick} {user} одобрен.", "allowed_dup": "Уже одобрен.",
 "disallowed": "{tick} Одобрение снято.", "not_found": "Не найдено.",
 "allowed_list": "{user} ОДОБРЕННЫЕ\n{items}", "empty": "— пусто —",
 "wl_list": "{shield} РАЗРЕШЁННЫЕ ССЫЛКИ\n{items}", "wl_ok": "{tick} Добавлено в белый список.", "wl_max": "{warn} Максимум 10 ссылок.",
 "wl_usage": "Использование: /whitelist &lt;url&gt;", "wl_rm": "{tick} Убрано из белого списка.",
 "bl_ok": "{tick} Добавлено в чёрный список.", "bl_rm": "{tick} Убрано из чёрного списка.",
 "bl_list": "{ban} ЗАПРЕЩЁННЫЕ СЛОВА\n{items}", "bl_usage": "Использование: /blacklist &lt;text&gt; или ответом на сообщение.",
 "t_users": "Пользователи", "t_bots": "Боты", "t_channels": "Каналы", "t_captions": "Подписи",
 "t_usernames": "@Юзернеймы", "t_admins": "Админы могут менять", "home": "Главная", "close": "Закрыть", "back": "Назад",
 "add": "✧₊ Добавить меня в чат ₊✧", "helpcmd": "Помощь и команды", "updates": "Обновления", "support": "Поддержка", "chlang": "Сменить язык",
}
S["ar"] = {
 "welcome": "<blockquote>تحياتي {name}،</blockquote>\n<blockquote expandable>✧ أهلاً بك في {bot} — بوت قوي وسريع لحماية المجموعات من الروابط\n✧ مصمم لمجموعات نظيفة • آمنة • خالية من السبام\n✧ يحذف تلقائياً الروابط وروابط الدعوة وإعلانات القنوات والمعرّفات غير المرغوبة\n✧ أضفني إلى مجموعتك وامنحني صلاحية <b>Delete Messages</b>\n" + DIV + "\n✧ اضغط على المساعدة لعرض جميع الأوامر والميزات</blockquote>",
 "groups_only": "{warn} /settings يعمل في <b>المجموعات فقط</b>.\n~\n~أضفني إلى مجموعتك واستخدمه هناك.\n~أرسل /help لعرض الأوامر المتاحة.",
 "no_perm": "{cross} غير مسموح لك بهذا الإجراء.",
 "settings": "{gear} لوحة سياسة الروابط\n\nاضغط للتبديل. {tick} = محظور، {cross} = مسموح.\nالمعتمدون: {au} · روابط القائمة البيضاء: {wl} · كلمات القائمة السوداء: {bl}",
 "lang_pick": "{globe} اختر لغة هذه المجموعة",
 "lang_set": "تم تحديث اللغة.",
 "deleted": "{ban} {user}، الروابط غير مسموحة هنا.",
 "deleted_bl": "{ban} {user}، هذه الكلمة/العبارة في القائمة السوداء.",
 "need_admin": "{warn} اجعلني مشرفاً مع صلاحية <b>Delete Messages</b> وإلا لن أتمكن من حذف الروابط.",
 "help": "{gear} مركز التحكم\n\n{help} الأوامر الأساسية\n/settings — فتح لوحة سياسة الروابط\n/language — تغيير لغة المجموعة\n/allowed — عرض المعتمدين\n/whitelist — عرض الروابط المسموحة\n\n{crown} إدارة المستخدمين\n/allow — اعتماد مستخدم\n/disallow — إزالة الاعتماد\n/whitelist &lt;url&gt; — السماح برابط (حد أقصى 10)\n/rwhitelist &lt;url&gt; — إزالة من القائمة البيضاء\n\n{ban} القائمة السوداء الذكية\n/blacklist &lt;text&gt; — حظر كلمة/عبارة (أو بالرد)\n/rblacklist &lt;n|text&gt; — إزالة من القائمة السوداء\n/blacklisted — عرض كل الكلمات المحظورة\n\n{user} يمكن لمالك المجموعة السماح للمشرفين بتعديل إعدادات البوت أو منعهم.",
 "live": "{rocket} ROOHIREMOV يعمل الآن!\n\nبوت ذكي وسريع لحماية المجموعات يحافظ على محادثاتك نظيفة وآمنة.\n\n{diamond} لا يمكن لأي مستخدم إرسال روابط\n{diamond} لا يمكن لأي بوت إرسال روابط\n{diamond} يحذف الروابط الخارجية تلقائياً\n{diamond} يدعم فلترة روابط المستخدمين والبوتات والقنوات والتعليقات\n{diamond} مالك المجموعة يتحكم بالقواعد\n{diamond} يمكن السماح للمعتمدين عبر /allow\n\nأضفني إلى مجموعتك وابتعد عن سبام الروابط.",
 "need_target": "رُدّ على مستخدم أو أرسل معرّفه.",
 "allowed_ok": "{tick} تم اعتماد {user}.", "allowed_dup": "معتمد بالفعل.",
 "disallowed": "{tick} تمت إزالة الاعتماد.", "not_found": "غير موجود.",
 "allowed_list": "{user} المعتمدون\n{items}", "empty": "— فارغ —",
 "wl_list": "{shield} الروابط المسموحة\n{items}", "wl_ok": "{tick} تمت الإضافة للقائمة البيضاء.", "wl_max": "{warn} الحد الأقصى 10 روابط.",
 "wl_usage": "الاستخدام: /whitelist &lt;url&gt;", "wl_rm": "{tick} تمت الإزالة من القائمة البيضاء.",
 "bl_ok": "{tick} تمت الإضافة للقائمة السوداء.", "bl_rm": "{tick} تمت الإزالة من القائمة السوداء.",
 "bl_list": "{ban} الكلمات المحظورة\n{items}", "bl_usage": "الاستخدام: /blacklist &lt;text&gt; أو بالرد على رسالة.",
 "t_users": "المستخدمون", "t_bots": "البوتات", "t_channels": "القنوات", "t_captions": "التعليقات",
 "t_usernames": "@المعرّفات", "t_admins": "للمشرفين التعديل", "home": "الرئيسية", "close": "إغلاق", "back": "رجوع",
 "add": "✧₊ أضفني إلى محادثتك ₊✧", "helpcmd": "المساعدة والأوامر", "updates": "التحديثات", "support": "الدعم", "chlang": "تغيير اللغة",
}
S["es"] = {
 "welcome": "<blockquote>Saludos {name},</blockquote>\n<blockquote expandable>✧ Bienvenido a {bot} — un bot potente y rápido de protección contra enlaces\n✧ Creado para grupos limpios • seguros • sin spam\n✧ Elimina automáticamente enlaces, invitaciones, promos de canales y usernames no deseados\n✧ Añádeme a un grupo y dame permiso de <b>Delete Messages</b>\n" + DIV + "\n✧ Usa ayuda para ver todos los comandos y funciones</blockquote>",
 "groups_only": "{warn} /settings funciona <b>solo en grupos</b>.\n~\n~Añádeme a tu grupo y úsalo allí.\n~Envía /help para ver los comandos.",
 "no_perm": "{cross} No tienes permiso para hacer esto.",
 "settings": "{gear} PANEL DE POLÍTICA DE ENLACES\n\nToca para cambiar. {tick} = bloqueado, {cross} = permitido.\nAprobados: {au} · Enlaces en lista blanca: {wl} · Palabras en lista negra: {bl}",
 "lang_pick": "{globe} ELIGE EL IDIOMA DE ESTE GRUPO",
 "lang_set": "Idioma actualizado.",
 "deleted": "{ban} {user}, los enlaces no están permitidos aquí.",
 "deleted_bl": "{ban} {user}, esa palabra/frase está en la lista negra.",
 "need_admin": "{warn} Hazme admin con permiso de <b>Delete Messages</b>, si no, no puedo borrar enlaces.",
 "help": "{gear} CENTRO DE CONTROL\n\n{help} COMANDOS ESENCIALES\n/settings — abrir el panel de política de enlaces\n/language — cambiar el idioma del grupo\n/allowed — ver usuarios aprobados\n/whitelist — ver enlaces permitidos\n\n{crown} GESTIÓN DE USUARIOS\n/allow — aprobar a un usuario\n/disallow — quitar aprobación\n/whitelist &lt;url&gt; — permitir un enlace (máx. 10)\n/rwhitelist &lt;url&gt; — quitar de la lista blanca\n\n{ban} LISTA NEGRA INTELIGENTE\n/blacklist &lt;text&gt; — bloquear palabra/frase (o responder)\n/rblacklist &lt;n|text&gt; — quitar de la lista negra\n/blacklisted — ver todas las palabras bloqueadas\n\n{user} El dueño del grupo puede permitir o impedir que los admins editen los ajustes del bot.",
 "live": "{rocket} ¡ROOHIREMOV YA ESTÁ ACTIVO!\n\nUn bot inteligente y rápido de protección de grupos para mantener tus chats limpios y seguros.\n\n{diamond} Ningún usuario puede enviar enlaces\n{diamond} Ningún bot puede enviar enlaces\n{diamond} Elimina enlaces externos automáticamente\n{diamond} Filtra enlaces de usuarios, bots, canales y descripciones\n{diamond} El dueño del grupo controla las reglas\n{diamond} Se puede permitir a usuarios aprobados con /allow\n\nAñádeme a tu grupo y mantén lejos el spam de enlaces.",
 "need_target": "Responde a un usuario o envía un ID de usuario.",
 "allowed_ok": "{tick} {user} aprobado.", "allowed_dup": "Ya está aprobado.",
 "disallowed": "{tick} Aprobación eliminada.", "not_found": "No encontrado.",
 "allowed_list": "{user} USUARIOS APROBADOS\n{items}", "empty": "— vacío —",
 "wl_list": "{shield} ENLACES PERMITIDOS\n{items}", "wl_ok": "{tick} Añadido a la lista blanca.", "wl_max": "{warn} Máximo 10 enlaces.",
 "wl_usage": "Uso: /whitelist &lt;url&gt;", "wl_rm": "{tick} Quitado de la lista blanca.",
 "bl_ok": "{tick} Añadido a la lista negra.", "bl_rm": "{tick} Quitado de la lista negra.",
 "bl_list": "{ban} PALABRAS BLOQUEADAS\n{items}", "bl_usage": "Uso: /blacklist &lt;text&gt; o responde a un mensaje.",
 "t_users": "Usuarios", "t_bots": "Bots", "t_channels": "Canales", "t_captions": "Descripciones",
 "t_usernames": "@Usernames", "t_admins": "Admins pueden editar", "home": "Inicio", "close": "Cerrar", "back": "Atrás",
 "add": "✧₊ Añádeme a tu chat ₊✧", "helpcmd": "Ayuda y comandos", "updates": "Novedades", "support": "Soporte", "chlang": "Cambiar idioma",
}
S["fr"] = {
 "welcome": "<blockquote>Salutations {name},</blockquote>\n<blockquote expandable>✧ Bienvenue sur {bot} — un bot puissant et rapide de protection contre les liens\n✧ Conçu pour des groupes propres • sûrs • sans spam\n✧ Supprime automatiquement les liens, invitations, promos de chaînes et pseudos indésirables\n✧ Ajoutez-moi à un groupe et donnez-moi la permission <b>Delete Messages</b>\n" + DIV + "\n✧ Utilisez l'aide pour voir toutes les commandes et fonctions</blockquote>",
 "groups_only": "{warn} /settings fonctionne <b>uniquement dans les groupes</b>.\n~\n~Ajoutez-moi à votre groupe et utilisez-le là-bas.\n~Envoyez /help pour voir les commandes.",
 "no_perm": "{cross} Vous n'avez pas le droit de faire cela.",
 "settings": "{gear} PANNEAU DE POLITIQUE DES LIENS\n\nAppuyez pour changer. {tick} = bloqué, {cross} = autorisé.\nApprouvés : {au} · Liens en liste blanche : {wl} · Mots en liste noire : {bl}",
 "lang_pick": "{globe} CHOISISSEZ LA LANGUE DU GROUPE",
 "lang_set": "Langue mise à jour.",
 "deleted": "{ban} {user}, les liens ne sont pas autorisés ici.",
 "deleted_bl": "{ban} {user}, ce mot/cette phrase est en liste noire.",
 "need_admin": "{warn} Faites de moi un admin avec la permission <b>Delete Messages</b>, sinon je ne peux pas supprimer les liens.",
 "help": "{gear} CENTRE DE CONTRÔLE\n\n{help} COMMANDES ESSENTIELLES\n/settings — ouvrir le panneau de politique des liens\n/language — changer la langue du groupe\n/allowed — voir les utilisateurs approuvés\n/whitelist — voir les liens autorisés\n\n{crown} GESTION DES UTILISATEURS\n/allow — approuver un utilisateur\n/disallow — retirer l'approbation\n/whitelist &lt;url&gt; — autoriser un lien (max 10)\n/rwhitelist &lt;url&gt; — retirer de la liste blanche\n\n{ban} LISTE NOIRE INTELLIGENTE\n/blacklist &lt;text&gt; — bloquer un mot/une phrase (ou répondre)\n/rblacklist &lt;n|text&gt; — retirer de la liste noire\n/blacklisted — voir tous les mots bloqués\n\n{user} Le propriétaire du groupe peut autoriser ou empêcher les admins de modifier les réglages du bot.",
 "live": "{rocket} ROOHIREMOV EST MAINTENANT EN LIGNE !\n\nUn bot intelligent et rapide de protection des groupes pour garder vos discussions propres et sûres.\n\n{diamond} Aucun utilisateur ne peut envoyer de liens\n{diamond} Aucun bot ne peut envoyer de liens\n{diamond} Supprime automatiquement les liens externes\n{diamond} Filtre les liens des utilisateurs, bots, chaînes et légendes\n{diamond} Le propriétaire du groupe contrôle les règles\n{diamond} Les approuvés peuvent être autorisés avec /allow\n\nAjoutez-moi à votre groupe et gardez le spam de liens à distance.",
 "need_target": "Répondez à un utilisateur ou envoyez un ID.",
 "allowed_ok": "{tick} {user} approuvé.", "allowed_dup": "Déjà approuvé.",
 "disallowed": "{tick} Approbation retirée.", "not_found": "Introuvable.",
 "allowed_list": "{user} UTILISATEURS APPROUVÉS\n{items}", "empty": "— vide —",
 "wl_list": "{shield} LIENS AUTORISÉS\n{items}", "wl_ok": "{tick} Ajouté à la liste blanche.", "wl_max": "{warn} Maximum 10 liens.",
 "wl_usage": "Utilisation : /whitelist &lt;url&gt;", "wl_rm": "{tick} Retiré de la liste blanche.",
 "bl_ok": "{tick} Ajouté à la liste noire.", "bl_rm": "{tick} Retiré de la liste noire.",
 "bl_list": "{ban} MOTS BLOQUÉS\n{items}", "bl_usage": "Utilisation : /blacklist &lt;text&gt; ou répondez à un message.",
 "t_users": "Utilisateurs", "t_bots": "Bots", "t_channels": "Chaînes", "t_captions": "Légendes",
 "t_usernames": "@Pseudos", "t_admins": "Admins peuvent modifier", "home": "Accueil", "close": "Fermer", "back": "Retour",
 "add": "✧₊ Ajoutez-moi à votre chat ₊✧", "helpcmd": "Aide & Commandes", "updates": "Actualités", "support": "Support", "chlang": "Changer de langue",
}
S["bn"] = {
 "welcome": "<blockquote>নমস্কার {name},</blockquote>\n<blockquote expandable>✧ {bot}-এ স্বাগতম — একটি শক্তিশালী ও দ্রুত লিংক প্রোটেকশন বট\n✧ পরিষ্কার • নিরাপদ • স্প্যামমুক্ত গ্রুপের জন্য তৈরি\n✧ লিংক, ইনভাইট লিংক, চ্যানেল প্রমো ও অবাঞ্ছিত ইউজারনেম নিজে থেকেই মুছে ফেলে\n✧ আমাকে গ্রুপে যোগ করুন এবং <b>Delete Messages</b> অনুমতি দিন\n" + DIV + "\n✧ সব কমান্ড ও ফিচার দেখতে হেল্প চাপুন</blockquote>",
 "groups_only": "{warn} /settings শুধু <b>গ্রুপে</b> কাজ করে।\n~\n~আমাকে আপনার গ্রুপে যোগ করে সেখানে ব্যবহার করুন।\n~কমান্ড দেখতে /help পাঠান।",
 "no_perm": "{cross} আপনার এটি করার অনুমতি নেই।",
 "settings": "{gear} লিংক পলিসি প্যানেল\n\nবদলাতে ট্যাপ করুন। {tick} = ব্লক, {cross} = অনুমোদিত।\nঅনুমোদিত ইউজার: {au} · হোয়াইটলিস্ট লিংক: {wl} · ব্ল্যাকলিস্ট শব্দ: {bl}",
 "lang_pick": "{globe} এই গ্রুপের ভাষা বেছে নিন",
 "lang_set": "ভাষা বদলানো হয়েছে।",
 "deleted": "{ban} {user}, এখানে লিংক পাঠানো নিষেধ।",
 "deleted_bl": "{ban} {user}, এই শব্দ/বাক্য ব্ল্যাকলিস্টে আছে।",
 "need_admin": "{warn} আমাকে <b>Delete Messages</b> অনুমতি সহ অ্যাডমিন করুন, নাহলে আমি লিংক মুছতে পারব না।",
 "help": "{gear} কন্ট্রোল সেন্টার\n\n{help} প্রয়োজনীয় কমান্ড\n/settings — লিংক পলিসি প্যানেল খুলুন\n/language — গ্রুপের ভাষা বদলান\n/allowed — অনুমোদিত ইউজার দেখুন\n/whitelist — অনুমোদিত লিংক দেখুন\n\n{crown} ইউজার ম্যানেজমেন্ট\n/allow — ইউজারকে অনুমোদন দিন\n/disallow — অনুমোদন সরান\n/whitelist &lt;url&gt; — একটি লিংক অনুমোদন (সর্বোচ্চ ১০)\n/rwhitelist &lt;url&gt; — হোয়াইটলিস্ট থেকে সরান\n\n{ban} স্মার্ট ব্ল্যাকলিস্ট\n/blacklist &lt;text&gt; — শব্দ/বাক্য ব্ল্যাকলিস্ট করুন (বা রিপ্লাই)\n/rblacklist &lt;n|text&gt; — ব্ল্যাকলিস্ট থেকে সরান\n/blacklisted — সব ব্ল্যাকলিস্ট শব্দ দেখুন\n\n{user} গ্রুপ ওনার চাইলে অ্যাডমিনদের বট সেটিংস বদলানো অনুমোদন বা বন্ধ করতে পারেন।",
 "live": "{rocket} ROOHIREMOV এখন লাইভ!\n\nআপনার চ্যাট পরিষ্কার ও নিরাপদ রাখতে একটি স্মার্ট ও দ্রুত গ্রুপ প্রোটেকশন বট।\n\n{diamond} কোনো ইউজার লিংক পাঠাতে পারবে না\n{diamond} কোনো বট লিংক পাঠাতে পারবে না\n{diamond} বাইরের লিংক নিজে থেকেই মুছে যায়\n{diamond} ইউজার, বট, চ্যানেল ও ক্যাপশন লিংক ফিল্টার\n{diamond} গ্রুপ ওনার নিয়ম নিয়ন্ত্রণ করেন\n{diamond} /allow দিয়ে অনুমোদিতদের অনুমতি দেওয়া যায়\n\nআমাকে আপনার গ্রুপে যোগ করুন এবং লিংক স্প্যাম দূরে রাখুন।",
 "need_target": "কোনো ইউজারকে রিপ্লাই করুন বা ইউজার ID পাঠান।",
 "allowed_ok": "{tick} {user} অনুমোদিত হয়েছে।", "allowed_dup": "আগে থেকেই অনুমোদিত।",
 "disallowed": "{tick} অনুমোদন সরানো হয়েছে।", "not_found": "পাওয়া যায়নি।",
 "allowed_list": "{user} অনুমোদিত ইউজার\n{items}", "empty": "— খালি —",
 "wl_list": "{shield} অনুমোদিত লিংক\n{items}", "wl_ok": "{tick} হোয়াইটলিস্টে যোগ হয়েছে।", "wl_max": "{warn} সর্বোচ্চ ১০টি লিংক।",
 "wl_usage": "ব্যবহার: /whitelist &lt;url&gt;", "wl_rm": "{tick} হোয়াইটলিস্ট থেকে সরানো হয়েছে।",
 "bl_ok": "{tick} ব্ল্যাকলিস্টে যোগ হয়েছে।", "bl_rm": "{tick} ব্ল্যাকলিস্ট থেকে সরানো হয়েছে।",
 "bl_list": "{ban} ব্ল্যাকলিস্ট শব্দ\n{items}", "bl_usage": "ব্যবহার: /blacklist &lt;text&gt; বা কোনো মেসেজে রিপ্লাই করুন।",
 "t_users": "ইউজার", "t_bots": "বট", "t_channels": "চ্যানেল", "t_captions": "ক্যাপশন",
 "t_usernames": "@ইউজারনেম", "t_admins": "অ্যাডমিন এডিট করতে পারবে", "home": "হোম", "close": "বন্ধ করুন", "back": "ফিরে যান",
 "add": "✧₊ আমাকে আপনার চ্যাটে যোগ করুন ₊✧", "helpcmd": "হেল্প ও কমান্ড", "updates": "আপডেট", "support": "সাপোর্ট", "chlang": "ভাষা বদলান",
}

def _fmt(lang: str, key: str, **kw) -> str:
    from .emojis import e
    txt = S.get(lang, {}).get(key) or S["en"][key]
    names = {n: e(n) for n in ("rocket","diamond","heart","shield","gear","warn","crown","user","ban","tick","globe","cross","bell","help")}
    names.update({"name": "User", "bot": "RoohiRemov"})
    names.update(kw)
    return txt.format(**names)

def t(lang: str, key: str, **kw) -> str:
    out = _fmt(lang, key, **kw)
    if key == "lang_set": return out
    out = "\n".join(l[1:] if l.startswith("~") else sc(l) for l in out.split("\n")).replace("\n\n\n", "\n\n")
    if key in NOQUOTE: return out
    tag = "<blockquote expandable>" if key in EXPAND else "<blockquote>"
    return f"{tag}{out}</blockquote>"

def tp(lang: str, key: str, **kw) -> str:
    """Plain text (popup/alert ke liye): tags hata ke."""
    return html.unescape(re.sub(r"<[^>]+>", "", t(lang, key, **kw)))


# ======================= v2: modules, help pages, new welcome =======================
MODNAMES = {"link": "Link-Filter", "phone": "Phone", "promo": "Promo", "nohash": "No-Hash", "nsfw": "NSFW",
            "abuse": "Abuse", "biomode": "Bio-Mode", "fonts": "Fonts", "forward": "Forward", "edit": "Edit",
            "mediadel": "Media-Del", "msgdel": "Msg-Del", "fsub": "F-Sub", "approve": "Approve",
            "autoapprove": "Auto-Approve", "echo": "Echo", "purge": "Purge"}
HELP_PAGES = [["link", "phone", "promo", "nohash", "nsfw", "abuse"],
              ["biomode", "fonts", "forward", "edit", "mediadel", "msgdel"],
              ["fsub", "approve", "autoapprove", "echo", "purge"]]
_NEWBTN = {"owner", "source", "next", "prev", "modules"}
BUTTONS.update(_NEWBTN); NOQUOTE.update(_NEWBTN | {"help_main"}); EXPAND.add("h_link")

S["en"].update({
 "welcome": "<blockquote>Hello {name}! 👋</blockquote>\n<blockquote expandable>I'm {bot}, your group's security bot, keeping chats clean and safe.\n\n☉ What I can do:\n➻ Block links, hashtags, phone numbers and promos\n➻ Delete edited messages, forwards and stylish fonts\n➻ Auto-delete messages and media\n➻ Force subscribe, bio link filter and abuse filter\n➻ Auto-approve join requests in groups & channels\n" + DIV + "\n⚠️ Get started:\n— Add me to your group\n— Make me an admin with <b>Delete Messages</b> permission\n— Tap Help to view all commands</blockquote>",
 "help_main": "☉ BOT COMMAND HELP :\n\n<blockquote>{gear} Here you'll find details for all available plugins and features.</blockquote>\n<blockquote>👇 Tap the buttons below to view help for each module :</blockquote>",
 "owner": "Owner", "source": "Source", "next": "Next ▶️", "prev": "◀️ Back", "modules": "Modules",
 "modules_title": "{gear} MODULES PANEL\n\nTap to toggle. {tick} = on, {cross} = off.\nMedia-Del: {md}s · Msg-Del: {sd}s · F-Sub: {fs}\nTimers: /mediadel, /msgdel · Channel: /fsub",
 "h_phone": "{gear} PHONE FILTER\n\nDeletes messages that contain phone numbers.\n\n/phone on|off — enable or disable\nAdmins and approved users are exempt.",
 "h_promo": "{gear} PROMO FILTER\n\nDeletes promotions: promo keywords (paid promotion, join my channel, follow me...), @channel / @group usernames and forwards from channels.\n\n/promo on|off",
 "h_nohash": "{gear} NO-HASH\n\nDeletes messages that contain #hashtags.\n\n/nohash on|off",
 "h_nsfw": "{gear} NSFW FILTER\n\nDeletes messages with adult / NSFW keywords (text and captions only — images are not scanned).\n\n/nsfw on|off",
 "h_abuse": "{gear} ABUSE FILTER\n\nDeletes abusive words (built-in list + your own words).\n\n/abuse on|off\n/addabuse &lt;word&gt; — add word\n/rmabuse &lt;word&gt; — remove word\n/abusewords — list your words",
 "h_biomode": "{gear} BIO-MODE\n\nDeletes messages from users who have a link in their Telegram bio.\n\n/biomode on|off",
 "h_fonts": "{gear} FONTS FILTER\n\nDeletes messages written in stylish / fancy unicode fonts (bold-italic letters, small caps, fullwidth, circled...).\n\n/fonts on|off",
 "h_forward": "{gear} FORWARD FILTER\n\nDeletes forwarded messages.\n\n/forward on|off",
 "h_edit": "{gear} EDIT FILTER\n\nDeletes a message when the user edits it after sending (stops 'send clean, edit in a link' tricks).\n\n/edit on|off",
 "h_mediadel": "{gear} MEDIA-DEL\n\nAuto-deletes media (photos, videos, files, stickers, voice, GIFs) after N seconds.\n\n/mediadel &lt;seconds|off&gt; — min 5",
 "h_msgdel": "{gear} MSG-DEL\n\nAuto-deletes every member message after N seconds.\n\n/msgdel &lt;seconds|off&gt; — min 5",
 "h_fsub": "{gear} FORCE SUBSCRIBE\n\nMembers must join your channel before they can chat. Make me admin in that channel first.\n\n/fsub @channel — set\n/fsub off — disable",
 "h_approve": "{gear} APPROVE\n\nApproved users bypass ALL filters.\n\n/approve — reply to a user or send an ID\n/unapprove — remove approval\n/approved — list approved users",
 "h_autoapprove": "{gear} AUTO-APPROVE\n\nAutomatically approves join requests in groups AND channels (default: ON). Make me admin with <b>Invite Users</b> permission.\n\n/autoapprove on|off — works in channels too",
 "h_echo": "{gear} ECHO\n\nMake me say something.\n\n/echo &lt;text&gt; — or reply to a message to copy it",
 "h_purge": "{gear} PURGE\n\nDelete many messages at once: reply to the first message you want gone and send /purge. Everything from there to your command is removed (max 1000).",
 "mod_on": "{tick} {mod}: ON — /{cmd} off", "mod_off": "{cross} {mod}: OFF — /{cmd} on",
 "timed_off": "{tick} {mod} disabled.", "timed_set": "{tick} {mod} set to {n}s.",
 "timed_usage": "{mod}: {cur}s (0 = off)\nUsage: /{cmd} &lt;seconds|off&gt; (min 5)",
 "fsub_set": "{tick} Force subscribe set to {chan}.", "fsub_off": "{tick} Force subscribe disabled.",
 "fsub_bad": "Usage: /fsub @channel | off", "fsub_show": "F-Sub: {cur}\nUsage: /fsub @channel | off",
 "fsub_need_admin": "{warn} Make me admin in that channel first (to check members).",
 "abuse_ok": "{tick} Added to abuse list.", "abuse_rm": "{tick} Removed from abuse list.",
 "abuse_list": "{ban} YOUR ABUSE WORDS\n{items}", "abuse_usage": "Usage: /addabuse &lt;word&gt;",
 "echo_usage": "Usage: /echo &lt;text&gt; or reply to a message.",
 "purge_usage": "Reply to the first message you want to delete, then send /purge.",
 "purge_done": "{tick} Purge done ({n} messages processed).",
 "deleted_mod": "{ban} {user}, your message was removed ({reason}).",
 "deleted_fsub": "{warn} {user}, join the channel first to chat here.",
 "approved_dm": "{tick} Hi {name}, your request to join <b>{chat}</b> was approved. Welcome! 🎉",
})
S["hg"].update({
 "welcome": "<blockquote>Hello {name}! 👋</blockquote>\n<blockquote expandable>Main {bot} hoon, aapke group ka security bot, chats ko clean aur safe rakhta hoon.\n\n☉ Main kya kar sakta hoon:\n➻ Links, hashtags, phone numbers aur promos block\n➻ Edited messages, forwards aur stylish fonts delete\n➻ Messages aur media auto-delete\n➻ Force subscribe, bio link filter aur abuse filter\n➻ Groups & channels me join requests auto-approve\n" + DIV + "\n⚠️ Shuru kaise karein:\n— Mujhe apne group me add karo\n— Mujhe <b>Delete Messages</b> permission ke saath admin banao\n— Saare commands dekhne ke liye Help dabao</blockquote>",
 "help_main": "☉ BOT COMMAND HELP :\n\n<blockquote>{gear} Yahan aapko saare plugins aur features ki details milengi.</blockquote>\n<blockquote>👇 Har module ki help dekhne ke liye neeche ke buttons dabao :</blockquote>",
 "owner": "Owner", "source": "Source", "next": "Next ▶️", "prev": "◀️ Back", "modules": "Modules",
 "modules_title": "{gear} MODULES PANEL\n\nToggle karne ke liye tap karo. {tick} = on, {cross} = off.\nMedia-Del: {md}s · Msg-Del: {sd}s · F-Sub: {fs}\nTimers: /mediadel, /msgdel · Channel: /fsub",
 "h_phone": "{gear} PHONE FILTER\n\nPhone number wale messages delete karta hai.\n\n/phone on|off — chalu ya band\nAdmins aur approved users exempt hain.",
 "h_promo": "{gear} PROMO FILTER\n\nPromotion delete karta hai: promo keywords (paid promotion, join my channel, follow me...), @channel / @group usernames aur channels se forward.\n\n/promo on|off",
 "h_nohash": "{gear} NO-HASH\n\n#hashtag wale messages delete karta hai.\n\n/nohash on|off",
 "h_nsfw": "{gear} NSFW FILTER\n\nAdult / NSFW keywords wale messages delete karta hai (sirf text aur captions — images scan nahi hoti).\n\n/nsfw on|off",
 "h_abuse": "{gear} ABUSE FILTER\n\nGaali wale words delete karta hai (built-in list + aapke apne words).\n\n/abuse on|off\n/addabuse &lt;word&gt; — word jodo\n/rmabuse &lt;word&gt; — word hatao\n/abusewords — apne words dekho",
 "h_biomode": "{gear} BIO-MODE\n\nJinke Telegram bio me link hai unke messages delete karta hai.\n\n/biomode on|off",
 "h_fonts": "{gear} FONTS FILTER\n\nStylish / fancy unicode fonts me likhe messages delete karta hai (bold-italic, small caps, fullwidth, circled...).\n\n/fonts on|off",
 "h_forward": "{gear} FORWARD FILTER\n\nForward kiye hue messages delete karta hai.\n\n/forward on|off",
 "h_edit": "{gear} EDIT FILTER\n\nUser message edit kare to delete kar deta hai (pehle clean bhej ke baad me link edit karne wali trick rokta hai).\n\n/edit on|off",
 "h_mediadel": "{gear} MEDIA-DEL\n\nMedia (photo, video, file, sticker, voice, GIF) N seconds baad auto-delete.\n\n/mediadel &lt;seconds|off&gt; — min 5",
 "h_msgdel": "{gear} MSG-DEL\n\nMembers ka har message N seconds baad auto-delete.\n\n/msgdel &lt;seconds|off&gt; — min 5",
 "h_fsub": "{gear} FORCE SUBSCRIBE\n\nChat karne se pehle members ko aapka channel join karna padega. Pehle mujhe us channel me admin banao.\n\n/fsub @channel — set karo\n/fsub off — band karo",
 "h_approve": "{gear} APPROVE\n\nApproved users pe SAARE filters nahi lagte.\n\n/approve — user ko reply karo ya ID bhejo\n/unapprove — approval hatao\n/approved — list dekho",
 "h_autoapprove": "{gear} AUTO-APPROVE\n\nGroups AUR channels me join requests apne aap approve karta hai (default: ON). Mujhe <b>Invite Users</b> permission ke saath admin banao.\n\n/autoapprove on|off — channel me bhi chalta hai",
 "h_echo": "{gear} ECHO\n\nMujhse kuch bulwao.\n\n/echo &lt;text&gt; — ya kisi message ko reply karke copy karwao",
 "h_purge": "{gear} PURGE\n\nEk saath bahut messages delete: jis message se delete karna hai usko reply karke /purge bhejo. Wahan se aapke command tak sab hat jata hai (max 1000).",
 "mod_on": "{tick} {mod}: ON — /{cmd} off", "mod_off": "{cross} {mod}: OFF — /{cmd} on",
 "timed_off": "{tick} {mod} band kar diya.", "timed_set": "{tick} {mod} {n}s pe set ho gaya.",
 "timed_usage": "{mod}: {cur}s (0 = off)\nUse karo: /{cmd} &lt;seconds|off&gt; (min 5)",
 "fsub_set": "{tick} Force subscribe {chan} pe set ho gaya.", "fsub_off": "{tick} Force subscribe band kar diya.",
 "fsub_bad": "Use karo: /fsub @channel | off", "fsub_show": "F-Sub: {cur}\nUse karo: /fsub @channel | off",
 "fsub_need_admin": "{warn} Pehle mujhe us channel me admin banao (members check karne ke liye).",
 "abuse_ok": "{tick} Abuse list me add ho gaya.", "abuse_rm": "{tick} Abuse list se hata diya.",
 "abuse_list": "{ban} AAPKE ABUSE WORDS\n{items}", "abuse_usage": "Use karo: /addabuse &lt;word&gt;",
 "echo_usage": "Use karo: /echo &lt;text&gt; ya kisi message ko reply karo.",
 "purge_usage": "Jis message se delete karna hai usko reply karke /purge bhejo.",
 "purge_done": "{tick} Purge ho gaya ({n} messages process hue).",
 "deleted_mod": "{ban} {user}, aapka message hata diya gaya ({reason}).",
 "deleted_fsub": "{warn} {user}, yahan chat karne ke liye pehle channel join karo.",
 "approved_dm": "{tick} Hi {name}, <b>{chat}</b> me aapki join request approve ho gayi. Welcome! 🎉",
})
for _l in S:                       # purana "help" = Link-Filter module help (translations safe rehte hain)
    if "help" in S[_l]: S[_l]["h_link"] = S[_l]["help"]


# ======================= v3: ping, group /start, broadcast, new live post =======================
MODNAMES["broadcast"] = "Broadcast"
HELP_PAGES[2].append("broadcast")
BUTTONS.add("addch"); NOQUOTE.update({"addch", "group_start"})

S["en"].update({
 "addch": "✧₊ Add me to your channel ₊✧",
 "ping": "🏓 PONG!\n⚡ Latency: {ms} ms\n⏱ Uptime: {up}\n🤖 Bot: {bot}",
 "group_start": "<blockquote>Hello {name}! 👋</blockquote>\n<blockquote>I'm {bot}, your group's security bot.\n✧ Links, phone numbers, promos & more are removed automatically\n✧ Make me admin with <b>Delete Messages</b> permission\n✧ /settings to configure · /help for all commands</blockquote>",
 "live": "{rocket} ROOHIREMOV IS NOW LIVE!\n\nA smart & fast all-in-one group protection bot to keep your chats clean and safe.\n\n{diamond} Blocks links, phone numbers, hashtags & promos\n{diamond} Abuse, NSFW, bio-link & stylish-font filters\n{diamond} Deletes forwards & edited messages\n{diamond} Auto-delete messages & media\n{diamond} Force subscribe\n{diamond} Auto-approve join requests (groups & channels)\n{diamond} Whitelist, blacklist & approved users\n{diamond} 10 languages\n\nAdd me to your group or channel and keep it clean.",
 "h_broadcast": "{gear} BROADCAST (owner only)\n\n/broadcast &lt;text&gt; — send to ALL users, groups & channels\n/broadcast -user &lt;text&gt; — users only\n/broadcast -group &lt;text&gt; — groups & channels only\nReply to any message with /broadcast to copy it (media & formatting kept).\n/live — send the bot launch post (with Add buttons)\n/live -user | -group\n/stats — users, groups, deleted, approved\n\nDead chats are removed automatically.",
})
S["hg"].update({
 "addch": "✧₊ Mujhe apne channel me add karo ₊✧",
 "ping": "🏓 PONG!\n⚡ Latency: {ms} ms\n⏱ Uptime: {up}\n🤖 Bot: {bot}",
 "group_start": "<blockquote>Hello {name}! 👋</blockquote>\n<blockquote>Main {bot} hoon, aapke group ka security bot.\n✧ Links, phone numbers, promos aur bahut kuch apne aap hat jate hain\n✧ Mujhe <b>Delete Messages</b> permission ke saath admin banao\n✧ Setup ke liye /settings · saare commands ke liye /help</blockquote>",
 "live": "{rocket} ROOHIREMOV AB LIVE HAI!\n\nEk smart & fast all-in-one group protection bot jo aapki chats ko clean aur safe rakhta hai.\n\n{diamond} Links, phone numbers, hashtags & promos block\n{diamond} Abuse, NSFW, bio-link & stylish-font filters\n{diamond} Forwards & edited messages delete\n{diamond} Messages & media auto-delete\n{diamond} Force subscribe\n{diamond} Join requests auto-approve (groups & channels)\n{diamond} Whitelist, blacklist & approved users\n{diamond} 10 languages\n\nMujhe apne group ya channel me add karo aur clean rakho.",
 "h_broadcast": "{gear} BROADCAST (sirf owner)\n\n/broadcast &lt;text&gt; — SAARE users, groups & channels ko bhejo\n/broadcast -user &lt;text&gt; — sirf users\n/broadcast -group &lt;text&gt; — sirf groups & channels\nKisi bhi message ko reply karke /broadcast bhejo to wo copy hoga (media & formatting ke saath).\n/live — bot ka launch post (Add buttons ke saath)\n/live -user | -group\n/stats — users, groups, deleted, approved\n\nDead chats apne aap hat jate hain.",
})

S["en"]["h_broadcast"] = S["en"]["h_broadcast"].replace("\n/stats", "\n/autopromo daily|once|off — live post at 7:00 AM (IST)\n/stats")
S["hg"]["h_broadcast"] = S["hg"]["h_broadcast"].replace("\n/stats", "\n/autopromo daily|once|off — subah 7:00 baje live post (IST)\n/stats")
