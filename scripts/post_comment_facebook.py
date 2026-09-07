"""
Post first comment containing repository link under the published Facebook post.
Includes headed Chrome execution, clipboard insertion, and live DOM comment verification.
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

COMMENT_TEXT = "Full open-source Skill definition, ISO/PDCA reference architecture, and copy-paste prompt:\n👉 GitHub: https://github.com/productaivn-wq/FileGovernance-Skill"


def run():
    print(f"[INFO] Navigating to post: {POST_URL}")
    print(f"[INFO] Comment text: {COMMENT_TEXT}")

    with sync_playwright() as p:
        print("[INFO] Launching headed Chrome browser for thaero comment...")
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

        page.goto(POST_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Locate comment box
        print("[INFO] Locating comment input box...")
        comment_box = None
        for _ in range(15):
            candidates = page.locator(
                "div[role='textbox'][aria-label*='Comment' i], div[role='textbox'][aria-label*='bình luận' i], div[contenteditable='true'][aria-label*='Comment' i], div[contenteditable='true'][aria-label*='bình luận' i]"
            ).all()
            for cb in candidates:
                try:
                    if cb.is_visible():
                        comment_box = cb
                        break
                except Exception:
                    pass
            if comment_box:
                break
            page.wait_for_timeout(1000)

        if not comment_box:
            print("[WARN] Direct comment box not found on posts URL, checking photo view...")
            page.goto("https://www.facebook.com/photo/?fbid=10245641013630569", wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            candidates = page.locator(
                "div[role='textbox'][aria-label*='Comment' i], div[role='textbox'][aria-label*='bình luận' i], div[contenteditable='true']"
            ).all()
            for cb in candidates:
                try:
                    if cb.is_visible():
                        comment_box = cb
                        break
                except Exception:
                    pass

        if not comment_box:
            print("[ERROR] Comment box not found!")
            browser.close()
            return

        print("[INFO] Focusing comment box...")
        comment_box.click()
        page.wait_for_timeout(600)

        print("[INFO] Pasting comment via pyperclip...")
        pyperclip.copy(COMMENT_TEXT)
        try:
            page.evaluate("(text) => navigator.clipboard.writeText(text)", COMMENT_TEXT)
        except Exception:
            pass

        page.keyboard.press("Control+v")
        page.wait_for_timeout(1500)

        # Pre-submit assertion
        inserted_text = comment_box.inner_text()
        print(f"[VERIFY] Inserted comment text: {inserted_text[:60]}... (length: {len(inserted_text)})")
        if "github.com/productaivn-wq/FileGovernance-Skill" not in inserted_text:
            print("[WARN] Paste did not insert link, typing directly via keyboard...")
            comment_box.fill(COMMENT_TEXT)
            page.wait_for_timeout(1000)

        print("[ACTION] Submitting comment via Enter key...")
        comment_box.press("Enter")
        page.wait_for_timeout(5000)

        # Live DOM verification of the posted comment
        body_text = page.locator("body").inner_text()
        has_repo_in_comments = "github.com/productaivn-wq/FileGovernance-Skill" in body_text
        print(f"[VERIFY] Live DOM Comment Verification: repo link present = {has_repo_in_comments}")

        screenshot_path = str(WORKSPACE_DIR / "references" / "facebook_comment_verified.png")
        page.screenshot(path=screenshot_path)
        print(f"[INFO] Saved comment verification screenshot to {screenshot_path}")

        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        browser.close()
        print("[DONE] Comment posting complete.")


if __name__ == "__main__":
    run()
