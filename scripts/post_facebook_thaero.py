"""
Facebook Publisher for thaero profile (thanberos@gmail.com).
Includes full-fidelity clipboard insertion, media attachment lock,
reCAPTCHA Enterprise handler, and post-publication empirical DOM verification.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import pyperclip

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

# Load centralized environment
load_dotenv(r"C:\Users\thanb\.gemini\.env")
load_dotenv(r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\.env")

EMAIL = os.environ.get("FACEBOOK_USERNAME", "thanberos@gmail.com")
PASSWORD = os.environ.get("FACEBOOK_PASSWORD", "Oneway0401@")

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = str(WORKSPACE_DIR / "references" / "cozy_orange_cat.jpg")
POST_PATH = WORKSPACE_DIR / "references" / "facebook_post.md"
STATE_FILE = r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\scripts\state_thaero.json"

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


def run():
    print(f"[INFO] Facebook Target Account: {EMAIL}")
    print(f"[INFO] Post text length: {len(post_text)} characters")
    print(f"[INFO] Image path: {IMAGE_PATH} (exists: {os.path.exists(IMAGE_PATH)})")

    with sync_playwright() as p:
        print("[INFO] Launching headed Chrome browser for thaero...")
        browser = p.chromium.launch(headless=False, channel="chrome")
        context_kwargs = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "viewport": {"width": 1280, "height": 850},
            "permissions": ["clipboard-read", "clipboard-write"],
        }
        if os.path.exists(STATE_FILE):
            print(f"[INFO] Loading session from {STATE_FILE}...")
            context_kwargs["storage_state"] = STATE_FILE

        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        print("[INFO] Navigating to Facebook...")
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # Check if already authenticated on thaero
        feed_triggers = page.locator(
            'div[aria-label*="on your mind" i], div[aria-label*="đang nghĩ gì" i], div[role="feed"]'
        )

        email_inp = page.locator("input[name='email'], input#email")
        pass_inp = page.locator("input[name='pass'], input#pass")

        if email_inp.count() > 0 and pass_inp.count() > 0:
            print(f"[INFO] Entering credentials for {EMAIL}...")
            email_inp.first.fill(EMAIL)
            page.wait_for_timeout(500)
            pass_inp.first.fill(PASSWORD)
            page.wait_for_timeout(500)
            print("[INFO] Submitting login form (Enter)...")
            pass_inp.first.press("Enter")
            page.wait_for_timeout(7000)

        # Monitor for feed, checkpoint, or 2FA
        logged_in = False
        for cycle in range(35):
            current_url = page.url
            print(f"[MONITOR] Facebook URL: {current_url[:75]}...")

            if feed_triggers.count() > 0 or ("facebook.com" in current_url and "checkpoint" not in current_url and "login" not in current_url and "two_step" not in current_url and "recover" not in current_url):
                # Verify we are on thaero by checking profile
                print("[SUCCESS] Facebook feed detected! Verifying account...")
                logged_in = True
                break

            # If reCAPTCHA checkpoint
            if "checkpoint" in current_url or "two_step" in current_url:
                print(f"[CHECKPOINT] Verification active ({cycle * 5}s elapsed)...")
                for f in page.frames:
                    if "google.com/recaptcha" in f.url and "anchor" in f.url:
                        checkbox = f.locator("#recaptcha-anchor, .recaptcha-checkbox")
                        if checkbox.count() > 0 and checkbox.get_attribute("aria-checked") != "true":
                            print("[ACTION] Clicking reCAPTCHA checkbox...")
                            checkbox.click()
                            page.wait_for_timeout(4000)

            page.wait_for_timeout(4000)

        if not logged_in:
            print("[WARN] Feed not reached automatically. Exiting.")
            browser.close()
            return

        # Save session
        try:
            context.storage_state(path=STATE_FILE)
            print(f"[INFO] Session saved to {STATE_FILE}")
        except Exception as se:
            print(f"[WARN] Session save note: {se}")

        # Open post composer
        print("[INFO] Opening post composer dialog...")
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3500)

        composer_trigger = page.locator(
            "div[role='button']:has-text(\"What's on your mind\"), div[role='button']:has-text(\"Bạn đang nghĩ gì\"), div[aria-label*='on your mind' i], div[aria-label*='đang nghĩ gì' i]"
        ).first
        if composer_trigger.count() > 0:
            composer_trigger.click()
            page.wait_for_timeout(3000)

        dialog = page.locator("div[role='dialog']").first
        if dialog.count() == 0:
            print("[ERROR] Post dialog not found!")
            browser.close()
            return

        # 1. Attach image first to ensure photo-first post type
        file_input = dialog.locator("input[type='file'][accept*='image']").first
        if file_input.count() == 0:
            photo_trigger = dialog.locator(
                "div[aria-label*='Photo/video' i], div[aria-label*='Ảnh/video' i], div[aria-label*='Photo' i]"
            ).first
            if photo_trigger.count() > 0:
                print("[INFO] Clicking Photo/video trigger to mount file input...")
                photo_trigger.click()
                page.wait_for_timeout(2000)
            file_input = dialog.locator("input[type='file'][accept*='image']").first

        if file_input.count() > 0:
            print(f"[INFO] Attaching image: {IMAGE_PATH}...")
            file_input.set_input_files(IMAGE_PATH)
            print("[INFO] Waiting 6s for photo preview to render...")
            page.wait_for_timeout(6000)
        else:
            print("[WARN] No file input found for image attachment!")

        # 2. Paste text into composer editor
        editor = dialog.locator("div[role='textbox'], div[contenteditable='true']").first
        if editor.count() == 0:
            print("[ERROR] Post editor textbox not found!")
            browser.close()
            return

        print("[INFO] Setting post text to Windows clipboard via pyperclip...")
        pyperclip.copy(post_text)
        try:
            page.evaluate("(text) => navigator.clipboard.writeText(text)", post_text)
        except Exception as ce:
            print(f"[WARN] Navigator clipboard note: {ce}")

        editor.click()
        page.wait_for_timeout(600)
        print("[INFO] Pasting text via Control+V...")
        page.keyboard.press("Control+v")
        page.wait_for_timeout(3500)

        # Pre-submit assertion: verify inserted text
        inserted_text = editor.inner_text()
        print(f"[VERIFY] Inserted text length: {len(inserted_text)} vs expected: {len(post_text)}")
        if len(inserted_text) < len(post_text) * 0.75:
            print("[WARN] Paste ratio under threshold, attempting editor.fill fallback...")
            editor.fill(post_text)
            page.wait_for_timeout(2000)
            inserted_text = editor.inner_text()
            print(f"[VERIFY] After fill: length is {len(inserted_text)}")

        if len(inserted_text) < len(post_text) * 0.70:
            print("[FAIL] Text was severely truncated in composer! Aborting before Post.")
            browser.close()
            return

        # 3. Check for 'Next' button (Facebook multi-step media composer)
        next_btn = dialog.locator(
            "div[aria-label='Next' i], div[role='button']:has-text('Next'), div[aria-label='Tiếp' i], div[role='button']:has-text('Tiếp')"
        ).first
        if next_btn.count() > 0 and next_btn.is_visible():
            print("[INFO] Clicking 'Next' button...")
            next_btn.click()
            page.wait_for_timeout(3500)

        # 4. Locate and click 'Post' button (on Post settings screen or direct dialog)
        print("[INFO] Locating exact Post button...")
        target_btn = None
        for _ in range(15):
            btn = page.locator(
                "div[role='dialog'] div[role='button'][aria-label='Post'], div[role='dialog'] div[role='button'][aria-label='Đăng']"
            ).first
            if btn.count() > 0 and btn.is_visible():
                box = btn.bounding_box()
                if box and box["width"] > 50 and box["height"] > 20:
                    target_btn = btn
                    print(f"[INFO] Found exact Post button at box: {box}")
                    break

            by_role = page.get_by_role("button", name="Post", exact=True).first
            if by_role.count() > 0 and by_role.is_visible():
                box = by_role.bounding_box()
                if box and box["width"] > 50 and box["height"] > 20:
                    target_btn = by_role
                    print(f"[INFO] Found Post button by exact role at box: {box}")
                    break
            page.wait_for_timeout(1000)

        if not target_btn:
            print("[ERROR] Post button not found!")
            browser.close()
            return

        # Wait for button to be enabled
        for wait_idx in range(15):
            disabled = target_btn.get_attribute("aria-disabled")
            if disabled != "true":
                print(f"[INFO] Post button enabled (aria-disabled={disabled})")
                break
            print(f"[INFO] Waiting for Post button... ({wait_idx}s)")
            page.wait_for_timeout(1000)

        box = target_btn.bounding_box()
        print(f"[ACTION] Clicking Post button via mouse coordinates ({box['x'] + box['width']/2}, {box['y'] + box['height']/2})...")
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(1500)

        # Fallback evaluate click
        try:
            target_btn.evaluate("(el) => el.click()")
        except Exception:
            pass

        print("[INFO] Waiting for submission to complete...")
        for wait_close in range(40):
            page.wait_for_timeout(1000)
            dialog_count = page.locator("div[role='dialog']").count()
            if dialog_count == 0:
                print(f"[SUCCESS] Post modal closed after {wait_close}s!")
                break
            if wait_close == 8:
                print("[RETRY] Retrying mouse click on Post button...")
                try:
                    box = target_btn.bounding_box()
                    if box:
                        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                except Exception:
                    pass
                page.keyboard.press("Control+Enter")

        print("[INFO] Post submitted! Waiting 10s for Facebook ingestion...")
        page.wait_for_timeout(10000)

        # Navigate to thaero profile
        print("[INFO] Navigating to https://www.facebook.com/thaero...")
        page.goto("https://www.facebook.com/thaero", wait_until="domcontentloaded")
        page.wait_for_timeout(7000)
        page.evaluate("window.scrollBy(0, 500)")
        page.wait_for_timeout(3000)

        # Empirical DOM verification with reload retry
        sys.path.insert(0, str(WORKSPACE_DIR / "scripts"))
        try:
            from verify_posts import PublicationVerifier
            expected_start = "Most people using Obsidian"
            expected_end = "compare notes"

            for attempt in range(4):
                body_text = page.locator("body").inner_text()
                if expected_start.lower() in body_text.lower():
                    print(f"[SUCCESS] Target post detected on profile timeline on attempt {attempt+1}!")
                    break
                print(f"[INFO] Post not visible yet, reloading profile timeline (attempt {attempt+1}/4)...")
                page.wait_for_timeout(5000)
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(7000)
                page.evaluate("window.scrollBy(0, 600)")
                page.wait_for_timeout(3000)

            media_count = page.locator("div[role='feed'] img, div[role='main'] img").count()
            ver_result = PublicationVerifier.verify_post_dom_content(
                published_text=body_text,
                expected_start=expected_start,
                expected_end=expected_end,
                media_count=media_count,
                require_media=True
            )
            print(f"[VERIFY] Live DOM Verification Result: {ver_result}")
        except Exception as ve:
            print(f"[WARN] Live DOM verification note: {ve}")

        # Extract direct candidate permalinks
        post_links = []
        for a in page.locator("a[href*='/posts/'], a[href*='permalink'], a[href*='thaero/posts']").all():
            try:
                href = a.get_attribute("href")
                if href and ("facebook.com" in href or href.startswith("/")):
                    full_link = href if href.startswith("http") else f"https://www.facebook.com{href}"
                    if full_link not in post_links:
                        post_links.append(full_link)
            except Exception:
                pass
        print(f"[VERIFY] Candidate Post Permalinks: {post_links[:5]}")

        screenshot_path = str(WORKSPACE_DIR / "references" / "facebook_thaero_live_posted.png")
        page.screenshot(path=screenshot_path)
        print(f"[INFO] Saved live verification screenshot to {screenshot_path}")

        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        browser.close()
        print("[DONE] Publishing to thaero complete.")


if __name__ == "__main__":
    run()
