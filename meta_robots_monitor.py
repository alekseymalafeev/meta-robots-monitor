# Meta Robots Monitor by Malafeev Aleksey
# https://github.com/alekseymalafeev/meta-robots-monitor
# https://t.me/todaSE0

import random
import time
from datetime import datetime
from urllib.parse import urlparse

import openpyxl
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


UA_PROFILES = {
    "1": {
        "name": "Client",
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    "2": {
        "name": "Googlebot",
        "ua": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    },
    "3": {
        "name": "Googlebot Smartphone",
        "ua": "Mozilla/5.0 (Linux; Android 10; Pixel 5) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 "
              "(compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    },
    "4": {
        "name": "YandexBot",
        "ua": "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
    }
}

REQUEST_TIMEOUT = 20
MIN_SLEEP_SECONDS = 30
JITTER_RANGE = (-15, 15)


def build_headers(user_agent: str) -> dict:
    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }


def normalize_host(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    return host.replace(".", "_")


def get_page_info(url: str, headers: dict) -> tuple:
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        status_code = response.status_code

        if status_code != 200:
            return status_code, "N/A"

        soup = BeautifulSoup(response.text, "html.parser")
        meta_robots = soup.find("meta", attrs={"name": "robots"})
        robots_content = meta_robots.get("content", "Empty") if meta_robots else "Not found"

        return status_code, robots_content

    except requests.RequestException:
        return None, "N/A"


def save_to_excel(rows: list, filename: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Meta Robots Log"

    ws.append([
        "URL",
        "Datetime",
        "fetch_mode",
        "user_agent",
        "http_status",
        "meta_robots"
    ])

    for row in rows:
        ws.append(row)

    wb.save(filename)


def select_mode() -> dict:
    print("\nВыберите режим парсинга:")
    print("1 — Client (Desktop Browser)")
    print("2 — Googlebot")
    print("3 — Googlebot Smartphone")
    print("4 — YandexBot")

    mode = input("Ваш выбор (1–4): ").strip()
    if mode not in UA_PROFILES:
        raise ValueError("Некорректный выбор режима.")
    return UA_PROFILES[mode]


def get_interval_seconds() -> int:
    minutes = int(input("Введите периодичность парсинга (в минутах): "))
    return minutes * 60


def build_filename(url: str) -> str:
    host = normalize_host(url)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    return f"meta_robots_{host}_{timestamp}.xlsx"


def log_row(url: str, ua_profile: dict, status_code: int, robots_content: str) -> list:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        url,
        current_time,
        ua_profile["name"],
        ua_profile["ua"],
        status_code,
        robots_content
    ]


def calculate_sleep_time(base_interval_sec: int) -> int:
    jitter = random.randint(*JITTER_RANGE)
    return max(MIN_SLEEP_SECONDS, base_interval_sec + jitter)


def main():
    print("=== Meta Robots Monitor ===")
    url = input("Введите URL страницы: ").strip()

    try:
        ua_profile = select_mode()
        base_interval_sec = get_interval_seconds()
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    headers = build_headers(ua_profile["ua"])
    filename = build_filename(url)
    data = []

    print(f"\nЛог будет сохранён в файл: {filename}\n")

    try:
        while True:
            status_code, robots_content = get_page_info(url, headers)

            row = log_row(url, ua_profile, status_code, robots_content)
            data.append(row)

            print(
                f"[{row[1]}] "
                f"UA={ua_profile['name']} | "
                f"HTTP={status_code} | "
                f"robots={robots_content}"
            )

            save_to_excel(data, filename)

            sleep_time = calculate_sleep_time(base_interval_sec)
            print(f"Следующий парсинг через ~{sleep_time // 60} мин.\n")

            for _ in tqdm(range(sleep_time), desc="Осталось времени", unit="с"):
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nВы приостановили работу скрипта. Сеанс завершён корректно.")
        if data:
            save_to_excel(data, filename)
        print(f"Итоговый файл сохранён: {filename}")


if __name__ == "__main__":
    main()