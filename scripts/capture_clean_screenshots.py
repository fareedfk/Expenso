import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def capture_all():
    print("Capturing live screenshots for presentation...")
    os.makedirs("scripts/screenshots", exist_ok=True)

    session = requests.Session()
    res = session.post("http://127.0.0.1:8000/api/auth/login", json={
        "email": "demo@expenso.com",
        "password": "demo123"
    })
    token = res.json().get("access_token")
    if not token:
        print("Login failed:", res.text)
        return

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--force-device-scale-factor=1")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=opts)

    # 1. Open app and inject token
    driver.get("http://127.0.0.1:8000")
    time.sleep(1)
    driver.execute_script(f"""
        localStorage.setItem('token', '{token}');
        localStorage.setItem('expenso_token', '{token}');
    """)
    driver.get("http://127.0.0.1:8000")
    time.sleep(2.5)

    # Dashboard screenshot
    driver.save_screenshot("scripts/screenshots/dashboard.png")
    print("Saved scripts/screenshots/dashboard.png")

    # 2. Analytics View
    driver.execute_script("""
        const nav = document.querySelector('[data-view="analytics"]') || document.querySelector('button[onclick*="analytics"]');
        if (nav) nav.click();
        else if (window.navigateToView) window.navigateToView('analytics');
    """)
    time.sleep(2)
    driver.save_screenshot("scripts/screenshots/analytics.png")
    print("Saved scripts/screenshots/analytics.png")

    # 3. Add Expense Modal open
    driver.execute_script("""
        const nav = document.querySelector('[data-view="dashboard"]') || document.querySelector('button[onclick*="dashboard"]');
        if (nav) nav.click();
        else if (window.navigateToView) window.navigateToView('dashboard');
    """)
    time.sleep(1)
    driver.execute_script("""
        const btn = document.querySelector('#btn-add-expense') || document.querySelector('.btn-primary') || document.querySelector('button[onclick*="openModal"]');
        if (btn) btn.click();
    """)
    time.sleep(1)
    driver.save_screenshot("scripts/screenshots/add_expense.png")
    print("Saved scripts/screenshots/add_expense.png")

    # 4. Swagger Docs
    driver.get("http://127.0.0.1:8000/docs")
    time.sleep(3)
    driver.save_screenshot("scripts/screenshots/swagger_docs.png")
    print("Saved scripts/screenshots/swagger_docs.png")

    driver.quit()
    print("All screenshots successfully captured!")

if __name__ == "__main__":
    capture_all()
