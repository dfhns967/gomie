from requests.exceptions import ProxyError, SSLError, ConnectionError, InvalidProxyURL, ChunkedEncodingError
import multiprocessing
from colorama import Fore, Style
from threading import Thread
import fake_useragent
import platform
import requests
import random
import string
import json
import time
import re
import os
from datetime import date
import webbrowser
import sys

cpm = 0
total = 0
valid = 0
invalid = 0
today = date.today()
proxies = "proxy.txt"
timeout = 3
config = False
runmain = 0

def cpmrunner():
    global valid
    global invalid
    global cpm
    while True:
        oldchecked = valid + invalid
        time.sleep(3)
        newchecked = invalid + valid
        cpm = (newchecked - oldchecked) * 60

if not os.path.isfile("proxy.txt"):
    with open("proxy.txt", "w") as fp:
        pass

if not os.path.exists("Results"):
    os.makedirs("Results")

def clear():
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")
    os.system("mode con: cols=105 lines=30")

def clear2():
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")
    logo()
    print("  ")
    print("  ")
    print("{} ╔══════════════════════════════════════════════════════════════════╗{}".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX))
    print("  ")

def logo():
    try:
        print(Fore.LIGHTBLUE_EX)
        msg = f"""
                              ███████╗███████╗ ██████╗ ██╗███████╗████████╗
                              ██╔════╝╚══███╔╝██╔════╝ ██║██╔════╝╚══██╔══╝
                              █████╗    ███╔╝ ██║  ███╗██║█████╗     ██║   
                              ██╔══╝   ███╔╝  ██║   ██║██║██╔══╝     ██║   
                              ███████╗███████╗╚██████╔╝██║██║        ██║   
                              ╚══════╝╚══════╝ ╚═════╝ ╚═╝╚═╝        ╚═╝\n
        """
        for l in msg:
            print(l, end="")
        print(Fore.RESET + "\t\t\t   Made By Zenux")

    except KeyboardInterrupt:
        sys.exit()

path, _ = os.path.split(__file__)
ua = fake_useragent.UserAgent()
proxy_file = open("proxy.txt", "r")
proxy_text = proxy_file.readlines()
not_checked = []

def headers():
    header = {
        "User-Agent" : ua.random,
        "content-type":"application/json",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }
    return header

def process():
    print(Fore.LIGHTMAGENTA_EX + " ║" + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + " ║" + Fore.LIGHTBLUE_EX + "   [+]" + Fore.LIGHTGREEN_EX + " Process Running Successfully... \n" + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + " ║" + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + " ╚════════════════" + Fore.LIGHTYELLOW_EX + " GiftCode " + Fore.LIGHTMAGENTA_EX + "══════" + Fore.LIGHTBLUE_EX + " Results " + Fore.LIGHTMAGENTA_EX + "════════"+ Fore.LIGHTYELLOW_EX + " Proxies " + Fore.LIGHTMAGENTA_EX + "════════╝" + Fore.RESET)
    print("  ")

def proxies():
    line = random.choice(proxy_text)
    ip = line.replace("\n", "")
    if str(ip).startswith("http"):
        pass
    else:
        https = "https://"+ip
        http = "http://"+ip
    proxy = {
        "https":https,
        "http":http
    }
    return proxy

def code():
    if option == 2:
        try:
            line = random.choice(codes)
            code = line.replace("\n", "")
            codes.remove(line)
        except IndexError:
            code = ("").join(random.choices(string.ascii_letters + string.digits, k=16))
    else:
        code = ("").join(random.choices(string.ascii_letters + string.digits, k=16))
    return code

def debug(code, text, proxy, show):
    global cpm
    global total
    global invalid
    global valid
    global config
    try:
        line = Fore.LIGHTYELLOW_EX + proxy["http"].split("//")[1]
        host = str(line.split(":")[0])
        port = str(line.split(":")[1])
    except:
        return
    if show.lower() == "error" or show.lower() == "message":
        not_checked.append(code)
        if config == False:
            return
        text = Fore.LIGHTYELLOW_EX + text + Fore.RESET
    if "Invalid" in text:
        text = Fore.RED + "   " + text
        total = total + 1
        invalid = invalid +1
        with open("Results/Bad.txt", "a+") as (f):
            f.writelines(code + " | BAD | " + str(today) + "\n")
    elif "Valided" in text:
        text = Fore.GREEN + "   " + text
        total = total + 1
        valid = valid + 1
        with open("Results/Hits.txt", "a+") as (f):
            f.writelines(code + " | HIT | " + str(today) + "\n")
    line = Fore.LIGHTYELLOW_EX + proxy["http"].split("//")[1] + Fore.RESET
    code = Fore.LIGHTYELLOW_EX + code  + Fore.RESET
    logo = str(Fore.LIGHTMAGENTA_EX + "> [Checker] - " + Fore.RESET)
    os.system("title " + " Discord Gift Checker by Teilaw - Checking [{}] - Hits: {} - Bad: {} - CPM [{}]".format(total, valid, invalid, cpm))
    print("{0:16} {1:26} {2:18} {3:22}".format(logo, code, text, line))

def run_checker(code, headers, proxy):
    try:
        global running
        running += 1
    except:
        running = 0
    s = requests.session()
    s.proxies = proxy
    url = "https://discordapp.com/api/v6/entitlements/gift-codes/{}?with_application=false&with_subscription_plan=true".format(code)
    try:
        rr = s.get(url, headers=headers, timeout=timeout)
        if "subscription_plan".lower() in (rr.text).lower():
            save(code)
            debug(code, "Valid", proxy, "Valid")
            running -= 1
            sys.exit()
        o = json.loads(rr.text)
        message = o["message"].lower()
        if message == "Unknown Gift Code".lower():
            debug(code, "Invalid", proxy, "Invalid")
        elif message == "You are being rate limited.".lower():
            debug(code, "Message", proxy, "Message")
        elif message == "Access denied":
            debug(code, "Message", proxy, "Message")
        else:
            print(rr.text)

    except KeyboardInterrupt:
        sys.exit()
    except ProxyError:
        debug(code,"   " + "ProxyEr", proxy, "Error")
    except SSLError:
        debug(code,"   " + "SSLErro", proxy, "Error")
    except ConnectionError:
        debug(code,"   " + "Connect", proxy, "Error")
    except InvalidProxyURL:
        debug(code,"   " + "ProxURL", proxy, "Error")
    except requests.exceptions.ReadTimeout:
        debug(code,"   " + "Timeout", proxy, "Error")
    except UnicodeError:
        debug(code,"   " + "UnError", proxy, "Error")
    except ChunkedEncodingError:
        debug(code,"   " + "Encodin", proxy, "Error")
    except json.decoder.JSONDecodeError:
        debug(code,"   " + "JDecode", proxy, "Decode")

    running -= 1
    sys.exit()

if __name__ == "__main__":
    try:
        clear()
        os.system("title " + " Discord Gift Checker by Teilaw ~ Waiting [0/0] - Hits: 0 - Bad: 0")
        logo()
        print("  ")
        print("  ")
        print("{} ╔════ Settings ════════════════════════════════╗{}".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX))
        print("{} ║{}".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX))
        print(Fore.LIGHTMAGENTA_EX +  " ║" + Fore.LIGHTBLUE_EX + " 1 - " + Fore.RESET + "[AUTO] Generator + Checker")
        print(Fore.LIGHTMAGENTA_EX +  " ║" + Fore.LIGHTBLUE_EX + " 2 - " + Fore.RESET + "Exit")
        print("{} ║{}".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX))
        print("{} ╚══════════════════════════════════════════════╝{}".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX))

        try:
            option = int(input("\n" +  Fore.LIGHTBLUE_EX + "   [?] - " + Fore.RESET + "Select Option (" + Fore.LIGHTBLUE_EX  + "1" + Fore.RESET + " or " + Fore.LIGHTBLUE_EX + "2" + Fore.RESET + "): "))
        except:
            print(Fore.LIGHTBLUE_EX + "   [!] - " + Fore.LIGHTRED_EX + "Invalid option.." + Fore.RESET)
            sys.exit()
        if option == 2:
            print("  ")
            print(Fore.LIGHTBLUE_EX + "   [!] - " + Fore.LIGHTRED_EX + "Thanks, BYE!" + Fore.RESET)
            time.sleep(2)
            sys.exit()
        print("  ")
        threads = int(input("\n" +  Fore.LIGHTBLUE_EX + "   [?] - " + Fore.RESET + "How many Threads ?: " + Fore.RESET))
        print("  ")
        print(Fore.LIGHTBLUE_EX + "   >"+ Fore.LIGHTGREEN_EX + " Starting.. Please Wait" + Fore.RESET)
        time.sleep(2)
        clear2()
        mythreads = []
        pr = multiprocessing.Process(target=process)
        pr.start()
        running = 0
        while True:
            if running <= threads:
                Thread(target=cpmrunner).start()
                x = Thread(target=run_checker, args=(code(), headers(), proxies(),))
                mythreads.append(x)
                x.start()
            else:
                time.sleep(1)
                for unchecked_code in not_checked:
                    x = Thread(target=run_checker, args=(code(), headers(), proxies(),))
                    mythreads.append(x)
                    x.start()
                    not_checked.remove(unchecked_code)
    except KeyboardInterrupt:
        print("  ")
        print(Fore.LIGHTBLUE_EX + "   [!] - " + Fore.LIGHTRED_EX + "Thanks, BYE!" + Fore.RESET)
        time.sleep(2)
        sys.exit()
    except FileNotFoundError:
        print("  ")
        print(Fore.LIGHTBLUE_EX + "   [!] - " + Fore.LIGHTRED_EX + "Invalid File Path" + Fore.RESET)
        sys.exit()
