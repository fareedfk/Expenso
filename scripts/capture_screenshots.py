import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    print("Connecting to Expenso server...")
    session = requests.Session()
    reg_data = {
        "name": "Fareed Khilji",
        "email": "fareed@aietm.ac.in",
        "password": "Password123",
        "currency": "INR"
    }
    res = session.post("http://127.0.0.1:8000/api/auth/register", json=reg_data)
    if res.status_code != 200:
        res = session.post("http://127.0.0.1:8000/api/auth/login", json={
            "email": "fareed@aietm.ac.in",
            "password": "Password123"
        })

    token = res.json().get("access_token")
    if not token:
        print("Warning: Could not get token, status:", res.status_code, res.text)
        return

    headers = {"Authorization": f"Bearer {token}"}
    print("[OK] Logged in as Fareed Khilji!")

    # Populate realistic college project expenses
    sample_txs = [
        {"type": "income", "amount": 20000, "category": "Salary", "description": "Training Stipend", "payment_method": "Bank Transfer"},
        {"type": "expense", "amount": 2100, "category": "Food", "description": "Campus Canteen & Meals", "payment_method": "UPI"},
        {"type": "expense", "amount": 4500, "category": "Rent", "description": "Hostel & Utility Fee", "payment_method": "UPI"},
        {"type": "expense", "amount": 850, "category": "Transport", "description": "Bus & Metro Recharge", "payment_method": "UPI"},
        {"type": "expense", "amount": 1400, "category": "Education", "description": "Project Printout & Books", "payment_method": "Cash"},
        {"type": "expense", "amount": 600, "category": "Entertainment", "description": "Weekend Refreshment", "payment_method": "UPI"},
    ]
    for tx in sample_txs:
        session.post("http://127.0.0.1:8000/api/transactions/", json=tx, headers=headers)

    session.post("http://127.0.0.1:8000/api/budgets/", json={"category": "Food", "amount": 3500, "period": "monthly"}, headers=headers)
    session.post("http://127.0.0.1:8000/api/budgets/", json={"category": "Rent", "amount": 5000, "period": "monthly"}, headers=headers)

    os.makedirs("scripts/screenshots", exist_ok=True)

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=opts)

    # Load and login
    driver.get("http://127.0.0.1:8000")
    time.sleep(1)
    driver.execute_script(f"""
        localStorage.setItem('token', '{token}');
        localStorage.setItem('expenso_token', '{token}');
    """)
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)

    # 1. Dashboard
    driver.save_screenshot("scripts/screenshots/app_dashboard.png")
    print("Screenshot 1: app_dashboard.png saved")

    # 2. Analytics View
    driver.execute_script("if (window.navigateToView) window.navigateToView('analytics');")
    time.sleep(1.5)
    driver.save_screenshot("scripts/screenshots/app_analytics.png")
    print("Screenshot 2: app_analytics.png saved")

    # 3. Budgets View
    driver.execute_script("if (window.navigateToView) window.navigateToView('budgets');")
    time.sleep(1.5)
    driver.save_screenshot("scripts/screenshots/app_budgets.png")
    print("Screenshot 3: app_budgets.png saved")

    # 4. Swagger API Documentation
    driver.get("http://127.0.0.1:8000/docs")
    time.sleep(2)
    driver.save_screenshot("scripts/screenshots/app_swagger.png")
    print("Screenshot 4: app_swagger.png saved")

    driver.quit()
    print("SUCCESS: All 4 screenshots captured successfully!")

if __name__ == "__main__":
    main()
