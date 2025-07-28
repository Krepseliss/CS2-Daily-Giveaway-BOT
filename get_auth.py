from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # show browser so you can log in manually
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://skinsmonkey.com")
    input("Log in via Steam and press Enter when you're done...")

    context.storage_state(path="F:\\PROJECTS\\SkinsMonkey BOT\\auth.json")  # Save login session
    browser.close()