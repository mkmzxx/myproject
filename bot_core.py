from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import random
import time
from datetime import datetime
from utils import get_random_user_agent, get_random_proxy, get_target_url, log_session

def simulate_user_behavior(driver):
    scroll_count = 0
    click_count = 0
    try:
        # Scroll part
        time.sleep(2)
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_times = random.randint(2, 5)
        for i in range(scroll_times):
            scroll_position = (i + 1) * scroll_height / (scroll_times + 1)
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(random.uniform(1, 2))
            scroll_count += 1

        # Collecting visible links
        links = driver.find_elements(By.TAG_NAME, "a")
        visible_links = [link for link in links if link.is_displayed() and link.get_attribute("href")]

        # Click on random links between 2 to 6 times
        for _ in range(random.randint(3, 6)):
            if not visible_links:
                break
            link_to_click = random.choice(visible_links)
            href = link_to_click.get_attribute("href")
            original_window = driver.current_window_handle

            try:
                # 🟡 50% chance to hover over the link before clicking
                if random.random() < 0.5:
                    ActionChains(driver).move_to_element(link_to_click).perform()
                    time.sleep(random.uniform(0.5, 1.2))  # wait after hover

                # 🔵 30% chance to right-click and open in a new tab
                if random.random() < 0.3:
                    ActionChains(driver).context_click(link_to_click).perform()
                    time.sleep(1)
                    ActionChains(driver).send_keys("t").perform()  # press 't' to open in new tab
                    time.sleep(2)
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(random.uniform(6, 8))
                        driver.close()
                        driver.switch_to.window(original_window)
                else:
                    # Normal click
                    link_to_click.click()
                    time.sleep(random.uniform(1.5, 2.5))

                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(random.uniform(7, 9))
                        driver.close()
                        driver.switch_to.window(original_window)
                    else:
                        time.sleep(random.uniform(3, 7))
                        driver.back()

                click_count += 1
                visible_links.remove(link_to_click)  # Remove clicked link to avoid duplicate clicks
            except Exception as click_err:
                print(f"Click error on {href}: {click_err}")
                continue

    except Exception as e:
        print("ব্যবহারকারীর আচরণে সমস্যা:", e)

    return scroll_count, click_count

def run_bot(headless=True, proxy=None):
    user_agent = get_random_user_agent()
    options = ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print("Chrome চালু করতে সমস্যা:", e)
        return

    try:
        target_url = get_target_url()
        driver.get(target_url)
        time.sleep(5)
        scrolls, clicks = simulate_user_behavior(driver)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_session(timestamp, target_url, user_agent, proxy or "None", scrolls, clicks)
    except Exception as e:
        print("Session error:", e)
    finally:
        driver.quit()