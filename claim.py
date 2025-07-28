from playwright.sync_api import sync_playwright

def claim_entry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="F:\\PROJECTS\\SkinsMonkey BOT\\auth.json")
        page = context.new_page()

        print("🌐 Opening giveaway page...")
        page.goto("https://skinsmonkey.com/free-csgo-skins")
        page.wait_for_timeout(3000)

        try:
            # Step 1: Click 'Join Now'
            join_now = page.locator("div.base-button__label:has-text('Join Now')")
            if join_now.count() > 0:
                join_now.first.click()
                print("✅ Clicked 'Join Now'")
                page.wait_for_timeout(2000)

            # Step 2: Click giveaway modal
            container = page.locator("div.free-giveaway-requirements__body")
            if container.count() > 0:
                container.first.click()
                print("✅ Clicked giveaway container")
                page.wait_for_timeout(4000)

            # Step 2.5: Click "Free Entry" if present
            free_entry_section = page.locator("div.free-giveaway-requirement:has(span:text('Free Entry'))")
            if free_entry_section.count() > 0 and free_entry_section.first.is_visible():
                free_entry_section.first.click()
                print("🎟️ Clicked 'Free Entry' section")
                page.wait_for_timeout(3000)
            else:
                print("⚠️ 'Free Entry' section not found or not visible")


            # Step 3: Scroll the modal manually (in case it's off-screen)
            print("↕️ Scrolling the modal content...")
            page.evaluate("""() => {
                const scrollable = document.querySelector('.scrollable-content__body');
                if (scrollable) scrollable.scrollTop = scrollable.scrollHeight;
            }""")
            page.wait_for_timeout(8000)

            # Step 4: Try to find Claim button after scroll
            claim_button = page.locator("div.base-button.green:has(span:text('Claim'))")

            if claim_button.count() > 0:
                print("🟢 Claim button found, scrolling into view...")
                claim_button.first.scroll_into_view_if_needed()
                page.wait_for_timeout(1000)

                try:
                    # Try native click
                    claim_button.first.click(timeout=3000)
                    print("🖱️ Native click sent")

                    # Wait and check if button is gone or changed (basic feedback loop)
                    page.wait_for_timeout(3000)
                    still_exists = claim_button.first.is_visible()
                    if still_exists:
                        print("⚠️ Claim button still visible — retrying with JS click...")
                        # JavaScript fallback
                        page.evaluate("el => el.click()", claim_button.first)
                        page.wait_for_timeout(2000)
                    else:
                        print("🎉 Successfully claimed via native click!")

                except Exception as e:
                    print(f"⚠️ Native click failed: {e}")
                    print("➡️ Trying JS fallback click...")
                    page.evaluate("el => el.click()", claim_button.first)
                    page.wait_for_timeout(2000)

            else:
                print("❌ Claim button not found.")

        except Exception as e:
            print(f"❌ Native click failed: {e}")
            print("➡️ Trying JavaScript fallback...")

        # JS fallback if native click fails completely
        try:
            button_handle = claim_button.first
            page.evaluate("(element) => element.click()", button_handle)
            print("✅ JS click sent successfully")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"❌ JS click failed: {e}")

if __name__ == "__main__":
    claim_entry()
