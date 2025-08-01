import telebot
import numpy as np
from sklearn.cluster import KMeans

bot = telebot.TeleBot(" رمز التكوين ")

equations = np.array([
    [1, 7, 10],
    [1, 2, 1],
    [1, 0, 1],
    [1, -3, 2],
    [1, 4, 4],
    [1, 1, 1]
])

delta = equations[:,1]**2 - 4*equations[:,0]*equations[:,2]
delta = delta.reshape(-1,1)

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(delta)

cluster_labels = {}
for i in range(3):
    cluster_points = delta[kmeans.labels_ == i]
    avg = np.mean(cluster_points)
    if avg < 0:
        cluster_labels[i] = "جذور مركبة (دلتا سالب)"
    elif avg == 0:
        cluster_labels[i] = "جذر مكرر (دلتا صفر)"
    else:
        cluster_labels[i] = "جذور حقيقية مختلفة (دلتا موجب)"

def classify_equation(a, b, c):
    d = b**2 - 4*a*c
    cluster = kmeans.predict([[d]])[0]
    return d, cluster_labels[cluster]

# حالة كل مستخدم (chat_id) يخزن شو الخطوة اللي هو فيها
user_states = {}

# الخطوة 0 = بمرحّب وأسأل عن العملية
# الخطوة 1 = استلم أرقام الجمع
# الخطوة 2 = استلم أرقام الطرح
# الخطوة 3 = استلم معاملات المعادلة

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_states[chat_id] = 0
    bot.send_message(chat_id, "مرحباً! أنا بوت صغير 😄\nاختر العملية:\n1. جمع\n2. طرح\n3. تصنيف معادلة من الدرجة الثانية")

@bot.message_handler(func=lambda m: True)
def handle(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    # إذا المستخدم جديد ما بعت أمر /start
    if chat_id not in user_states:
        user_states[chat_id] = 0
        bot.send_message(chat_id, "أرسل /start لبدء التفاعل معي 😊")
        return
    
    state = user_states[chat_id]
    
    if state == 0:
        # ننتظر اختيار العملية 1 أو 2 أو 3
        if text == '1':
            user_states[chat_id] = 1
            bot.send_message(chat_id, "أرسل رقمين للجمع مفصولين بمسافة مثلا:\n5 7")
        elif text == '2':
            user_states[chat_id] = 2
            bot.send_message(chat_id, "أرسل رقمين للطرح مفصولين بمسافة مثلا:\n10 3")
        elif text == '3':
            user_states[chat_id] = 3
            bot.send_message(chat_id, "أرسل معاملات المعادلة الثلاثة مفصولين بمسافة مثلا:\n1 6 5")
        else:
            bot.send_message(chat_id, "الرجاء اختيار واحد من 1 أو 2 أو 3")
    
    elif state == 1:
        # جمع
        try:
            parts = text.split()
            if len(parts) != 2:
                raise ValueError
            num1 = float(parts[0])
            num2 = float(parts[1])
            result = num1 + num2
            bot.send_message(chat_id, f"النتيجة: {result}")
        except:
            bot.send_message(chat_id, "تأكد من إرسال رقمين مفصولين بمسافة مثل: 5 7")
        # رجع للحالة 0
        user_states[chat_id] = 0
        bot.send_message(chat_id, "اختر العملية التالية:\n1. جمع\n2. طرح\n3. تصنيف معادلة من الدرجة الثانية")

    elif state == 2:
        # طرح
        try:
            parts = text.split()
            if len(parts) != 2:
                raise ValueError
            num1 = float(parts[0])
            num2 = float(parts[1])
            result = num1 - num2
            bot.send_message(chat_id, f"النتيجة: {result}")
        except:
            bot.send_message(chat_id, "تأكد من إرسال رقمين مفصولين بمسافة مثل: 10 3")
        user_states[chat_id] = 0
        bot.send_message(chat_id, "اختر العملية التالية:\n1. جمع\n2. طرح\n3. تصنيف معادلة من الدرجة الثانية")
    
    elif state == 3:
        # تصنيف معادلة
        try:
            parts = text.split()
            if len(parts) != 3:
                raise ValueError
            a, b, c = map(float, parts)
            d, group = classify_equation(a, b, c)
            bot.send_message(chat_id, f"دلتا = {d}\nالتصنيف: {group}")
        except:
            bot.send_message(chat_id, "تأكد من إرسال 3 أرقام مفصولين بمسافة مثل: 1 6 5")
        user_states[chat_id] = 0
        bot.send_message(chat_id, "اختر العملية التالية:\n1. جمع\n2. طرح\n3. تصنيف معادلة من الدرجة الثانية")

bot.polling()
