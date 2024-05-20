import requests
def Send_telegram_message(token, chat_id , message):
    r = requests.post(f"https://api.telegram.org/bot{token}/SendMessage?chat_id={chat_id}&text={message}").json()
    if r["ok"]:
    	return "تم ارسال الرسالة"
    else:
    	return "حدث خطأ في ارسال الرسالة تاكد من المعلومات"
