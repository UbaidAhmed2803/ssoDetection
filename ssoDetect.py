import asyncio
from playwright.async_api import async_playwright
import re

SSO_KEYWORDS = [
    "sign in with google",
    "login with google",
    "continue with google",
    "use your google account",
    "google login",
    "log in with google",
    "signin with google",
    "sign in using google",
    "sign in via google"
]

async def check_sso_with_playwright(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(4000)

            content = await page.content()
            title = await page.title()
            sso_detected = False

            # Check keywords in DOM content
            content_lower = content.lower()
            if any(re.search(rf"\b{re.escape(k)}\b", content_lower) for k in SSO_KEYWORDS):
                sso_detected = True
                title += " (SSO Detected via Text)"

            # Attempt to click possible login buttons and check redirect
            login_buttons = await page.locator("a, button").all()
            for btn in login_buttons:
                try:
                    text = (await btn.inner_text()).lower()
                    if any(k in text for k in SSO_KEYWORDS):
                        await btn.click()
                        await page.wait_for_load_state("networkidle", timeout=7000)
                        final_url = page.url
                        if "accounts.google.com" in final_url:
                            sso_detected = True
                            title += " (SSO Detected via Redirect)"
                            break
                except:
                    continue

            if not sso_detected:
                title += " (No SSO Detected)"

            print(f"{url} → {title}")
            await browser.close()

    except Exception:
        print(f"{url} → Error Occurred")

async def main():
    with open("ttnsubdomains.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
        for url in urls:
            if not url.startswith("http"):
                url = "https://" + url
            await check_sso_with_playwright(url)

if __name__ == "__main__":
    asyncio.run(main())
