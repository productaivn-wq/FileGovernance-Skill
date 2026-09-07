import os
import sys
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# Load centralized environment
load_dotenv(r"C:\Users\thanb\.gemini\.env")
load_dotenv(r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\.env")

EMAIL = os.environ.get("LINKEDIN_USERNAME", "phuong.vnn.0401@gmail.com")
PASSWORD = os.environ.get("LINKEDIN_PASSWORD", "Oneway0401@")
TWOCAPTCHA_KEY = os.environ.get("TWOCAPTCHA_API_KEY", "7816a036f3210a789ca94b302d67b6df")

STATE_FILE = r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\scripts\state.json"
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = str(WORKSPACE_DIR / "references" / "zen_capybara_bath.jpg")
POST_PATH = WORKSPACE_DIR / "references" / "linkedin_post.md"

post_raw = POST_PATH.read_text(encoding="utf-8")
if "```markdown" in post_raw:
    post_text = post_raw.split("```markdown")[1].split("```")[0].strip()
else:
    post_text = post_raw.strip()

print(f"[INFO] Post text length: {len(post_text)} characters")
print(f"[INFO] Image path: {IMAGE_PATH} (exists: {os.path.exists(IMAGE_PATH)})")
print(f"[INFO] 2Captcha API Key present: {bool(TWOCAPTCHA_KEY)}")


def solve_recaptcha_enterprise(site_key: str, page_url: str) -> str:
    print(f"[2CAPTCHA] Submitting reCAPTCHA Enterprise challenge (key: {site_key[:8]}...)...")
    submit_url = "https://2captcha.com/in.php"
    params = {
        "key": TWOCAPTCHA_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": page_url,
        "enterprise": "1",
        "json": "1",
    }
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{submit_url}?{qs}", headers={"User-Agent": "JobHunterKit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    
    if res.get("status") != 1:
        raise RuntimeError(f"2Captcha submission failed: {res}")
    
    task_id = res["request"]
    print(f"[2CAPTCHA] Task ID received: {task_id}. Polling for solution...")
    
    poll_url = f"https://2captcha.com/res.php?key={TWOCAPTCHA_KEY}&action=get&id={task_id}&json=1"
    for elapsed in range(5, 125, 5):
        time.sleep(5)
        req = urllib.request.Request(poll_url, headers={"User-Agent": "JobHunterKit/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            poll_res = json.loads(resp.read().decode("utf-8"))
        
        if poll_res.get("status") == 1:
            token = poll_res["request"]
            print(f"[2CAPTCHA] Solved in {elapsed}s! Token received (len {len(token)})")
            return token
        
        if poll_res.get("request") != "CAPCHA_NOT_READY":
            raise RuntimeError(f"2Captcha error during polling: {poll_res}")
        
        print(f"[2CAPTCHA] Solving puzzle in progress ({elapsed}s elapsed)...")
    
    raise TimeoutError("2Captcha polling timed out after 120 seconds.")


def run():
    with sync_playwright() as p:
        print("[INFO] Launching headed Chrome browser...")
        browser = p.chromium.launch(headless=False, channel="chrome")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 850},
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        print("[INFO] Navigating to LinkedIn login...")
        page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)

        # Fill visible credentials
        for inp in page.locator("input[type='email']").all():
            box = inp.bounding_box()
            if box and box["width"] > 0:
                print(f"[INFO] Filling email: {EMAIL}")
                inp.click()
                inp.fill(EMAIL)
                break

        for inp in page.locator("input[type='password']").all():
            box = inp.bounding_box()
            if box and box["width"] > 0:
                print("[INFO] Filling password...")
                inp.click()
                inp.fill(PASSWORD)
                page.wait_for_timeout(500)
                inp.press("Enter")
                break

        print("[INFO] Credentials submitted. Monitoring for feed or security checkpoint...")
        page.wait_for_timeout(6000)

        logged_in = False
        for cycle in range(30):
            current_url = page.url
            print(f"[MONITOR] Current URL: {current_url[:70]}...")

            if "feed" in current_url:
                print("[SUCCESS] Feed detected! Successfully authenticated.")
                logged_in = True
                break

            if "checkpoint" in current_url or "challenge" in current_url:
                print("[CHECKPOINT] Security verification challenge detected!")
                
                # Check for captchaSiteKey in parent form
                sitekey = None
                key_el = page.locator("input[name='captchaSiteKey']")
                if key_el.count() > 0:
                    sitekey = key_el.first.get_attribute("value")
                
                if not sitekey:
                    sitekey = os.environ.get("LINKEDIN_RECAPTCHA_SITEKEY", "6Lc7CQMTAAAAAIL84V_tPRYEWZtljsJQJZ5jSijw")
                
                print(f"[CHECKPOINT] Using sitekey: {sitekey}")
                
                try:
                    token = solve_recaptcha_enterprise(sitekey, current_url)
                    print("[CHECKPOINT] Injecting solved token into challenge form...")
                    
                    # 1. Fill parent form input
                    page.evaluate(f"""
                        (function() {{
                            var tokenInput = document.querySelector('input[name="captchaUserResponseToken"]');
                            if (tokenInput) {{
                                tokenInput.value = '{token}';
                                console.log('[INJECT] tokenInput populated');
                            }}
                            var form = document.getElementById('captcha-challenge');
                            if (form) {{
                                console.log('[INJECT] Submitting captcha-challenge form');
                                form.submit();
                            }}
                        }})();
                    """)
                    
                    # 2. Also inject into internal frame if present
                    for frame in page.frames:
                        if "captchaInternal" in frame.url or frame.name == "captcha-internal":
                            try:
                                frame.evaluate(f"""
                                    (function() {{
                                        var el = document.getElementById('g-recaptcha-response');
                                        if (el) el.value = '{token}';
                                        window.parent.postMessage(JSON.stringify({{
                                            eventId: 'captchaResponseReceived',
                                            payload: {{ response: '{token}' }}
                                        }}), '*');
                                    }})();
                                """)
                                print("[CHECKPOINT] Injected into captchaInternal frame successfully")
                            except Exception as fe:
                                print(f"[WARN] Frame injection note: {fe}")
                    
                    print("[CHECKPOINT] Waiting for post-challenge verification response...")
                    page.wait_for_timeout(8000)
                    
                except Exception as ce:
                    print(f"[ERROR] 2Captcha solve failed: {ce}. User can solve manually in open Chrome window.")
                    page.wait_for_timeout(5000)
            else:
                page.wait_for_timeout(4000)

        if not logged_in and "feed" in page.url:
            logged_in = True

        if not logged_in:
            print("[WARN] Feed not reached within loop. Checking final page state...")
            if "feed" in page.url:
                logged_in = True
            else:
                print("[ERROR] Could not complete login. Exiting.")
                browser.close()
                return

        # Save session
        print(f"[INFO] Saving session state to {STATE_FILE}...")
        try:
            context.storage_state(path=STATE_FILE)
        except Exception as se:
            print(f"[WARN] Storage state error: {se}")

        # Navigate to share post
        print("[INFO] Navigating to LinkedIn post dialog...")
        page.goto("https://www.linkedin.com/feed/?shareActive=true", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        # Locate editor
        editor = page.locator("div[role='textbox'], div.ql-editor, div[contenteditable='true']")
        if editor.count() == 0:
            trigger = page.locator("button:has-text('Start a post'), button.share-box-feed-entry__trigger")
            if trigger.count() > 0:
                trigger.first.click()
                page.wait_for_timeout(2500)
            editor = page.locator("div[role='textbox'], div.ql-editor, div[contenteditable='true']")

        if editor.count() > 0:
            print("[INFO] Pasting post text...")
            target_editor = editor.first
            target_editor.click()
            target_editor.fill(post_text)
            page.wait_for_timeout(2000)
        else:
            print("[WARN] Editor not directly found, looking for alternative triggers...")

        # Attach image
        file_input = page.locator("input[type='file'][accept*='image']")
        if file_input.count() > 0:
            print(f"[INFO] Uploading image: {IMAGE_PATH}...")
            file_input.first.set_input_files(IMAGE_PATH)
            page.wait_for_timeout(4000)
            next_btn = page.locator("button:has-text('Next'), button[aria-label='Next'], button:has-text('Tiếp theo')")
            if next_btn.count() > 0 and next_btn.first.is_visible():
                print("[INFO] Clicking Next on image preview...")
                next_btn.first.click()
                page.wait_for_timeout(2500)

        # Click Post
        post_btn = page.locator("button.share-actions__primary-action, button:has-text('Post'), button:has-text('Đăng')").first
        if post_btn.count() > 0 and post_btn.is_visible() and not post_btn.is_disabled():
            print("[INFO] Submitting LinkedIn post...")
            post_btn.click()
            page.wait_for_timeout(7000)
            print("[SUCCESS] LinkedIn post successfully published!")
            
            screenshot_path = str(WORKSPACE_DIR / "references" / "linkedin_posted.png")
            page.screenshot(path=screenshot_path)
            print(f"[INFO] Screenshot saved to {screenshot_path}")
        else:
            print("[INFO] Post is pre-filled on your screen. You can review and click Post.")
            page.wait_for_timeout(15000)

        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        page.wait_for_timeout(3000)
        browser.close()
        print("[DONE] LinkedIn automation finished.")


if __name__ == "__main__":
    run()
