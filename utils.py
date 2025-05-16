import random
from fake_useragent import UserAgent
from datetime import datetime

# র‍্যান্ডম ইউজার এজেন্ট তৈরি করার ফাংশন
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# র‍্যান্ডম প্রক্সি বেছে নেওয়ার ফাংশন
import random

def get_random_proxy():
    try:
        with open("working_proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return random.choice(proxies) if proxies else None
    except FileNotFoundError:
        print("⚠️ working_proxies.txt ফাইল পাওয়া যায়নি!")
        return None

# config.txt থেকে টার্গেট URL নেওয়ার ফাংশন
def get_target_url():
    try:
        with open("config.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        return random.choice(urls) if urls else None
    except FileNotFoundError:
        return None

# লগ ফাইল লেখার ফাংশন
def log_session(timestamp, url, user_agent, proxy, scroll_count, click_count):
    log_entry = (
        f"[{timestamp}] Visited: {url} | "
        f"User-Agent: {user_agent} | "
        f"Proxy: {proxy or 'None'} | "
        f"Scrolls: {scroll_count} | "
        f"Clicks: {click_count}\n"
        + "-"*60 + "\n"
    )
    with open("session_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)