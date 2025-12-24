import telebot
import requests
import time

# আপনার পাঠানো স্ক্রিনশট থেকে সংগৃহীত সঠিক তথ্য
BOT_TOKEN = "8287589351:AAH_ENMT3Od1sQ2vttLUBgsIhaKuPBzC9ho" # আপনার নতুন বটের টোকেন
CHAT_ID = "-1003607510758" # আপনার নতুন গ্রুপের আইডি
API_TOKEN = "f3-Ydn5PUTxHTg==" # আপনার প্যানেলের এপিআই টোকেন (শেষে == সহ)

bot = telebot.TeleBot(BOT_TOKEN)

def check_and_send_otp():
    last_sent_otp = None
    print("বটটি এখন ওটিপি চেক করার জন্য সচল আছে...")
    
    while True:
        try:
            # প্যানেল থেকে ওটিপি চেক করার লিঙ্ক
            url = f"https://flysms.xyz/api/v2?action=getOrders&api_key={API_TOKEN}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # যদি প্যানেলে কোনো অর্ডার থাকে
                if data and isinstance(data, list):
                    latest_order = data[0]
                    otp_code = latest_order.get('sms', 'No SMS yet')
                    
                    # যদি নতুন কোনো ওটিপি পাওয়া যায় (পুরনোর সাথে না মিললে)
                    if otp_code != last_sent_otp and otp_code != 'No SMS yet':
                        message = f"📌 New OTP Received:\n\n💬 Code: {otp_code}\n👤 Owner: JAHANGIR"
                        bot.send_message(CHAT_ID, message)
                        last_sent_otp = otp_code
                        print(f"সফলভাবে ওটিপি গ্রুপে পাঠানো হয়েছে: {otp_code}")
            else:
                print(f"প্যানেলে সমস্যা: স্ট্যাটাস কোড {response.status_code}")
                
        except Exception as e:
            print(f"ভুল হয়েছে: {e}")
        
        # প্রতি ১০ সেকেন্ড পর পর প্যানেল চেক করবে
        time.sleep(10)

if __name__ == "__main__":
    check_and_send_otp()
