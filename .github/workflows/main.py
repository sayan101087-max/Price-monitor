import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# -------------------------------------------------
# อ่านค่าจาก GitHub Secrets
# -------------------------------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# -------------------------------------------------
# ฟังก์ชันแจ้งเตือน Telegram
# -------------------------------------------------
def send_alert(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# -------------------------------------------------
# ฟังก์ชันตรวจราคาสินค้า (Makro)
# -------------------------------------------------
def check_makro(url, last_price=None):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        name = soup.select_one("h1.product-name").get_text(strip=True)
        price = soup.select_one("span.price").get_text(strip=True)

        if last_price and price != last_price:
            send_alert(f"📢 Makro ราคาเปลี่ยน!\nสินค้า: {name}\nราคาใหม่: {price}\nลิงก์: {url}")

        return price

    except Exception as e:
        send_alert(f"❗ เกิดข้อผิดพลาด Makro\n{e}")

# -------------------------------------------------
# ฟังก์ชันตรวจราคาสินค้า (ไทวัสดุ)
# -------------------------------------------------
def check_thaiwatsadu(url, last_price=None):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        name = soup.select_one("h1").get_text(strip=True)
        price = soup.select_one(".price").get_text(strip=True)

        if last_price and price != last_price:
            send_alert(f"📢 ไทวัสดุ ราคาเปลี่ยน!\nสินค้า: {name}\nราคาใหม่: {price}\nลิงก์: {url}")

        return price

    except Exception as e:
        send_alert(f"❗ เกิดข้อผิดพลาด ไทวัสดุ\n{e}")

# -------------------------------------------------
# ฟังก์ชันตรวจราคาสินค้า (HomePro)
# -------------------------------------------------
def check_homepro(url, last_price=None):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        name = soup.select_one("h1").get_text(strip=True)
        price = soup.select_one(".price").get_text(strip=True)

        if last_price and price != last_price:
            send_alert(f"📢 HomePro ราคาเปลี่ยน!\nสินค้า: {name}\nราคาใหม่: {price}\nลิงก์: {url}")

        return price

    except Exception as e:
        send_alert(f"❗ เกิดข้อผิดพลาด HomePro\n{e}")


# -------------------------------------------------
# รายการสินค้าที่ต้องการตรวจสอบ
# (สามารถเพิ่มได้ไม่จำกัด)
# -------------------------------------------------
PRODUCTS = [
    {
        "name": "Makro Example",
        "url": "https://www.makro.pro/example/product",
        "checker": check_makro,
        "last_price": None
    },
    {
        "name": "Thai Watsadu Example",
        "url": "https://www.thaiwatsadu.com/example/product",
        "checker": check_thaiwatsadu,
        "last_price": None
    },
    {
        "name": "HomePro Example",
        "url": "https://www.homepro.co.th/p/EXAMPLE",
        "checker": check_homepro,
        "last_price": None
    }
]

# -------------------------------------------------
# เริ่มกระบวนการตรวจสอบทั้งหมด
# -------------------------------------------------
if __name__ == "__main__":
    send_alert("🔍 กำลังตรวจสอบราคาสินค้า...")

    for p in PRODUCTS:
        price = p["checker"](p["url"], p["last_price"])
        p["last_price"] = price

    send_alert("✅ ตรวจสอบราคาสินค้าเสร็จแล้ว")
