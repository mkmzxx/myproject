import os
import time
import threading
import sys
import requests
import random
from utils import get_random_proxy
from bot_core import run_bot

def normalize_proxy(p):
    if "://" in p:
        return p
    else:
        return "http://" + p

def is_proxy_working(proxy_url):
    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False

def test_proxies():
    print("🔎 proxy.txt ফাইল থেকে প্রক্সি চেক করা হচ্ছে...")
    try:
        with open("proxy.txt", "r") as f:
            raw_proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ proxy.txt ফাইল পাওয়া যায়নি!")
        return

    working_proxies = []
    for p in raw_proxies:
        full_proxy = normalize_proxy(p)
        if is_proxy_working(full_proxy):
            print(f"✅ Working: {full_proxy}")
            working_proxies.append(full_proxy)
        else:
            print(f"❌ Dead: {full_proxy}")

    with open("working_proxies.txt", "w") as f:
        for p in working_proxies:
            f.write(p + "\n")

    print(f"\n✅ মোট {len(working_proxies)}টি ওয়ার্কিং প্রক্সি সংরক্ষণ করা হয়েছে working_proxies.txt তে।")

def start_sessions_concurrently(session_count=2, use_proxy=True):
    threads = []
    for _ in range(session_count):
        proxy = get_random_proxy() if use_proxy else None
        t = threading.Thread(target=run_bot, kwargs={'headless': False, 'proxy': proxy})
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def main_menu():
    while True:
        print("\n=== মেইন মেনু ===")
        print("1. Proxy Test")
        print("2. Program Run")
        print("3. Exit")

        choice = input("আপনার অপশন দিন (1/2/3): ").strip()

        if choice == "1":
            test_proxies()

        elif choice == "2":
            try:
                session_count = int(input("❓ কতটি সেশন একসাথে চালাতে চান? (ডিফল্ট: 2): ") or 2)
                use_proxy = input("❓ আপনি কি প্রোক্সি ব্যবহার করতে চান? (y/n): ").strip().lower() == "y"
                print("🚀 বট চালু হচ্ছে...\n")
                while True:  # এখানে সেশনগুলো বারবার চলতে থাকবে যতক্ষণ না তুমি বন্ধ করবে
                    start_sessions_concurrently(session_count, use_proxy)
                    time.sleep(3)
            except Exception as e:
                print(f"⚠️ সমস্যা হয়েছে: {e}")

        elif choice == "3":
            print("👋 প্রোগ্রাম বন্ধ করা হচ্ছে...")
            sys.exit()

        else:
            print("⚠️ সঠিক অপশন দিন (1, 2, অথবা 3)!")

if __name__ == "__main__":
    main_menu()
