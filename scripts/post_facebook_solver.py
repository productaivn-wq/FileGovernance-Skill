import os
import sys
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

load_dotenv(r"C:\Users\thanb\.gemini\.env")
load_dotenv(r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\.env")

EMAIL = os.environ.get("FACEBOOK_USERNAME", "phuong.vnn.0401@gmail.com")
PASSWORD = os.environ.get("FACEBOOK_PASSWORD", "Oneway0401@")
TWOCAPTCHA_KEY = os.environ.get("TWOCAPTCHA_API_KEY", "7816a036f3210a789ca94b302d67b6df")

STATE_FILE = r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\scripts\state.json"
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = str(WORKSPACE_DIR / "references" / "cozy_orange_cat.jpg")
POST_PATH = WORKSPACE_DIR / "references" / "facebook_post.md"

post_raw = POST_PATH.read_text(encoding="utf-8")
if "## 🇺🇸 Version 1: English" in post_raw:
    part = post_raw.split("## 🇺🇸 Version 1: English")[1].split("## 🇻🇳 Version 2")[0]
    if "```markdown" in part:
        post_text = part.split("```markdown")[1].split("```")[0].strip()
    else:
        post_text = part.strip()
else:
    post_text = post_raw.strip()

post_text += "\n\n📸 (Photo completely unrelated to file architecture — just an absurdly cozy cat sleeping by a mechanical keyboard to soothe your soul before you tackle 3,000 unorganized files)."

print(f"[INFO] Facebook post text length: {len(post_text)} characters")
print(f"[INFO] Image path: {IMAGE_PATH} (exists: {os.path.exists(IMAGE_PATH)})")


def run():
    with sync_playwright() as p:
        print("[INFO] Launching headed Chrome browser for Facebook...")
        browser = p.chromium.launch(headless=False, channel="chrome")
        context_kwargs = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "viewport": {"width": 1280, "height": 850},
        }
        if os.path.exists(STATE_FILE):
            print(f"[INFO] Using authenticated session from {STATE_FILE}...")
            context_kwargs["storage_state"] = STATE_FILE

        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        print("[INFO] Navigating to Facebook...")
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3500)

        # Handle cookie consent dialogs if any
        consent_btns = page.locator(
            "button:has-text('Allow all cookies'), button:has-text('Cho phép tất cả cookie'), button:has-text('Accept all'), button:has-text('Chấp nhận tất cả')"
        )
        if consent_btns.count() > 0:
            print("[INFO] Dismissing cookie consent...")
            consent_btns.first.click()
            page.wait_for_timeout(1500)

        # Check for email input
        email_inp = page.locator("input[name='email'], input#email")
        pass_inp = page.locator("input[name='pass'], input#pass")

        if email_inp.count() > 0 and pass_inp.count() > 0:
            print(f"[INFO] Entering Facebook credentials ({EMAIL})...")
            email_inp.first.fill(EMAIL)
            page.wait_for_timeout(500)
            pass_inp.first.fill(PASSWORD)
            page.wait_for_timeout(500)
            
            print("[INFO] Submitting login form by pressing Enter...")
            pass_inp.first.press("Enter")
            
            print("[INFO] Login submitted. Monitoring for feed or checkpoint...")
            page.wait_for_timeout(6000)

        logged_in = False
        for cycle in range(30):
            current_url = page.url
            print(f"[MONITOR] Facebook URL: {current_url[:70]}...")

            feed_triggers = page.locator(
                "div[aria-label*='What\\'s on your mind' i], div[aria-label*='Bạn đang nghĩ gì' i], div[role='main']"
            )
            if feed_triggers.count() > 0 or "facebook.com/?sk=" in current_url:
                print("[SUCCESS] Facebook feed detected! Authenticated.")
                logged_in = True
                break

            if "checkpoint" in current_url or "two_factor" in current_url or "two_step" in current_url:
                print(f"[CHECKPOINT] Facebook checkpoint / 2FA screen active ({cycle * 5}s elapsed)...")
                
                # Check frames
                for i, f in enumerate(page.frames):
                    print(f"  Frame {i}: {f.url[:80]} (name={f.name})")
                    if "fbsbx.com" in f.url:
                        try:
                            Path(WORKSPACE_DIR / "references" / "fbsbx_frame.html").write_text(f.content(), encoding="utf-8")
                            print("  [INFO] Dumped fbsbx_frame.html successfully")
                        except Exception as de:
                            print(f"  [WARN] Could not dump fbsbx content: {de}")
                    
                    if "google.com/recaptcha" in f.url and "anchor" in f.url:
                        print("  [INFO] Found reCAPTCHA anchor frame!")
                        try:
                            # Try clicking the checkbox if not already checked
                            checkbox = f.locator("#recaptcha-anchor, .recaptcha-checkbox")
                            if checkbox.count() > 0:
                                checked = checkbox.get_attribute("aria-checked")
                                print(f"  [INFO] Checkbox aria-checked={checked}")
                                if checked != "true":
                                    print("  [ACTION] Clicking reCAPTCHA anchor checkbox...")
                                    checkbox.click()
                                    page.wait_for_timeout(3000)
                        except Exception as ce:
                            print(f"  [WARN] Checkbox click note: {ce}")

            page.wait_for_timeout(5000)

        if not logged_in:
            print("[WARN] Feed not reached automatically. Exiting.")
            browser.close()
            return

        try:
            context.storage_state(path=STATE_FILE)
        except Exception as se:
            print(f"[WARN] Storage state error: {se}")

        # Open post composer
        print("[INFO] Opening post composer dialog...")
        trigger = page.locator(
            "div[aria-label*='What\\'s on your mind' i], div[aria-label*='Bạn đang nghĩ gì' i], span:has-text('What\\'s on your mind'), span:has-text('Bạn đang nghĩ gì')"
        )
        if trigger.count() > 0:
            trigger.first.click()
            page.wait_for_timeout(3000)

        editor = page.locator("div[role='textbox'], div[contenteditable='true']").first
        if editor.count() > 0:
            print("[INFO] Typing post text...")
            editor.click()
            editor.fill(post_text)
            page.wait_for_timeout(2000)

        # Attach image
        file_input = page.locator("input[type='file'][accept*='image']")
        if file_input.count() > 0:
            print(f"[INFO] Attaching image: {IMAGE_PATH}...")
            file_input.first.set_input_files(IMAGE_PATH)
            print("[INFO] Waiting 6s for image upload to process...")
            page.wait_for_timeout(6000)

        # Click Post
        print("[INFO] Locating visible Facebook Post button...")
        target_btn = None
        for _ in range(15):
            candidates = page.locator(
                "div[aria-label='Post' i], div[aria-label='Đăng' i], div[role='button']:has-text('Post'), div[role='button']:has-text('Đăng')"
            ).all()
            for btn in candidates:
                try:
                    if btn.is_visible():
                        box = btn.bounding_box()
                        if box and box["width"] > 50 and box["height"] > 20:
                            target_btn = btn
                            print(f"[INFO] Found visible Post button at box: {box}")
                            break
                except Exception:
                    pass
            if target_btn:
                break
            page.wait_for_timeout(1000)

        if not target_btn:
            print("[WARN] Could not find visible Post button! Taking diagnostic screenshot...")
            page.screenshot(path=str(WORKSPACE_DIR / "references" / "facebook_diag.png"))
            return

        # Wait if aria-disabled
        for wait_idx in range(15):
            disabled = target_btn.get_attribute("aria-disabled")
            if disabled != "true":
                print(f"[INFO] Post button is ready (aria-disabled={disabled})")
                break
            print(f"[INFO] Waiting for Post button to enable... ({wait_idx}s)")
            page.wait_for_timeout(1000)

        box = target_btn.bounding_box()
        print(f"[INFO] Clicking Post button via mouse at ({box['x'] + box['width']/2}, {box['y'] + box['height']/2})...")
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(1500)

        # Also trigger evaluate click and force click as reinforcement
        try:
            target_btn.evaluate("(el) => el.click()")
        except Exception:
            pass

        print("[INFO] Monitoring for post submission...")
        for wait_close in range(25):
            page.wait_for_timeout(1000)
            try:
                if not target_btn.is_visible():
                    print(f"[SUCCESS] Post button disappeared after {wait_close}s! Submission complete.")
                    break
            except Exception:
                print(f"[SUCCESS] Target button detached! Submission complete.")
                break

            if wait_close == 6:
                print("[RETRY] Retrying mouse click and Ctrl+Enter...")
                box = target_btn.bounding_box()
                if box:
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.keyboard.press("Control+Enter")

        page.wait_for_timeout(6000)
        print("[INFO] Navigating to user profile (https://www.facebook.com/me)...")
        page.goto("https://www.facebook.com/me", wait_until="domcontentloaded")
        page.wait_for_timeout(7000)

        screenshot_path = str(WORKSPACE_DIR / "references" / "facebook_live_posted.png")
        page.screenshot(path=screenshot_path)
        print(f"[INFO] Profile screenshot saved to {screenshot_path}")

        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        page.wait_for_timeout(3000)
        browser.close()
        print("[DONE] Facebook automation finished.")


if __name__ == "__main__":
    run()
