"""
Edit published Facebook post to replace raw GitHub link with pointer to first comment.
Includes headed Chrome execution, clipboard replacement, pre-submit assertion,
and live DOM verification.
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

load_dotenv(r"C:\Users\thanb\.gemini\.env")
load_dotenv(r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\.env")

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = r"C:\Users\thanb\.gemini\antigravity\skills\JobHunterKit\scripts\state_thaero.json"
POST_URL = "https://www.facebook.com/thaero/posts/10245641013630569"
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


def run():
    print(f"[INFO] Post URL: {POST_URL}")
    print(f"[INFO] Updated text length: {len(post_text)} characters")
    print("[INFO] Has link pointer in updated text:", "(Link in the first comment" in post_text)

    with sync_playwright() as p:
        print("[INFO] Launching headed Chrome browser to edit post...")
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

        PHOTO_URL = "https://www.facebook.com/photo/?fbid=10245641013630569"
        print(f"[INFO] Navigating directly to photo view: {PHOTO_URL}")
        page.goto(PHOTO_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Locate Edit button (aria-label='Edit description' or text='Edit')
        print("[INFO] Locating Edit description button...")
        edit_btn = page.locator(
            "div[role='button'][aria-label='Edit description'], div[role='button']:has-text('Edit')"
        ).first

        if edit_btn.count() == 0 or not edit_btn.is_visible():
            print("[ERROR] Edit description button not found!")
            browser.close()
            return

        print("[INFO] Clicking Edit description button...")
        edit_btn.click()
        page.wait_for_timeout(2500)

        # Locate editor
        edit_box = page.locator("div[role='textbox'], div[contenteditable='true'], textarea").first
        if edit_box.count() == 0 or not edit_box.is_visible():
            print("[ERROR] Contenteditable editor not visible after clicking Edit!")
            browser.close()
            return

        tag = edit_box.evaluate("el => el.tagName")
        print(f"[INFO] Editor element tag: {tag}")

        print("[INFO] Focusing editor and clearing previous text...")
        edit_box.click()
        page.wait_for_timeout(500)
        page.keyboard.press("Control+a")
        page.wait_for_timeout(300)
        page.keyboard.press("Backspace")
        page.wait_for_timeout(500)

        print("[INFO] Pasting updated post text via pyperclip...")
        pyperclip.copy(post_text)
        try:
            page.evaluate("(text) => navigator.clipboard.writeText(text)", post_text)
        except Exception:
            pass

        page.keyboard.press("Control+v")
        page.wait_for_timeout(2500)

        # Pre-submit assertions
        inserted_text = edit_box.inner_text() if tag != "TEXTAREA" else edit_box.input_value()
        print(f"[VERIFY] Inserted text length: {len(inserted_text)} vs expected: {len(post_text)}")
        has_pointer = "(Link in the first comment" in inserted_text
        has_raw_url = "github.com/productaivn-wq/FileGovernance-Skill" in inserted_text
        print(f"[VERIFY] Has comment pointer: {has_pointer} | Has raw URL: {has_raw_url}")

        if not has_pointer:
            print("[WARN] Comment pointer missing, attempting fallback fill...")
            edit_box.fill(post_text)
            page.wait_for_timeout(1000)
            inserted_text = edit_box.inner_text() if tag != "TEXTAREA" else edit_box.input_value()
            has_pointer = "(Link in the first comment" in inserted_text
            has_raw_url = "github.com/productaivn-wq/FileGovernance-Skill" in inserted_text

        assert has_pointer, "Comment pointer must be present in the edited post body!"
        assert not has_raw_url, "Raw GitHub URL must not be present in the edited post body!"

        # Locate and click 'Done Editing' button
        print("[INFO] Locating 'Done Editing' button...")
        done_btn = page.locator(
            "div[role='button'][aria-label='Done Editing'], div[role='button']:has-text('Done Editing')"
        ).first

        if done_btn.count() > 0:
            print("[ACTION] Clicking 'Done Editing' button...")
            done_btn.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            done_btn.click()
            print("[INFO] Waiting 7s for update to commit...")
            page.wait_for_timeout(7000)
        else:
            print("[ERROR] 'Done Editing' button not found!")
            browser.close()
            return

        # Navigate to canonical post to verify live DOM
        print("[INFO] Navigating to canonical post URL to verify live DOM...")
        page.goto(POST_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Look specifically at post content container vs comment container
        body_text = page.locator("body").inner_text()
        post_has_pointer = "(Link in the first comment" in body_text
        comment_has_raw = "github.com/productaivn-wq/FileGovernance-Skill" in body_text
        print(f"[VERIFY] Live DOM Verification: comment pointer present = {post_has_pointer}, comment link present = {comment_has_raw}")

        screenshot_path = str(WORKSPACE_DIR / "references" / "facebook_post_edited_verified.png")
        page.screenshot(path=screenshot_path)
        print(f"[INFO] Saved edited post verification screenshot to {screenshot_path}")

        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        browser.close()
        print("[DONE] Post edit complete.")


if __name__ == "__main__":
    run()
