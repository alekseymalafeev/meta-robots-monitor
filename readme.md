# meta-robots-monitor

## 🇷🇺 Описание
Скрипт периодически запрашивает указанную страницу, фиксирует HTTP‑код ответа и значение метатега `robots`, сохраняя результаты в Excel.  
Поддерживает несколько профилей User‑Agent и добавляет небольшой случайный промежуток времени к интервалу запросов.

## 🇺🇸 Description
The script periodically checks a given web page, captures the HTTP status code and the `robots` meta tag content, and saves results to an Excel file.  
It supports multiple User‑Agent profiles and adds a small random jitter to the polling interval.

---

## 🚀 Features / Возможности
- User‑Agent profiles: Client, Googlebot, Googlebot Smartphone, YandexBot
- Periodic parsing with jitter
- Extracts `meta name="robots"`
- Saves to `.xlsx`

---

## 🛠 Requirements / Требования
- Python 3.8+
- requests
- beautifulsoup4
- openpyxl
- tqdm

---

## 📦 Installation / Установка
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage / Запуск
```bash
python meta_robots_monitor.py
```

При запуске нужно указать:
- URL
- профиль User‑Agent
- интервал в минутах

---

## 📁 Output / Результат
Создаётся файл вида:

`meta_robots_<host>_YYYY_MM_DD_HH_MM.xlsx`

**Колонки:**
- URL
- Datetime
- fetch_mode
- user_agent
- http_status
- meta_robots

---

## 📄 Example / Пример
```text
URL: https://example.com
Datetime: 2026-02-25 12:30:00
fetch_mode: Googlebot
user_agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
http_status: 200
meta_robots: index,follow
```

---

## 🧩 Notes / Примечания
- При остановке через `Ctrl+C` скрипт завершится корректно и сохранит файл.
- Интервал включает небольшую случайную задержку, чтобы запросы не были строго регулярными.