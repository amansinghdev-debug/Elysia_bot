import asyncio
from playwright.async_api import async_playwright


async def reel(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 👈 force visible!
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        print("✅ Opening page...")
        await page.goto("https://igram.world/reels-downloader", timeout=60000)

        print("✅ Filling URL...")
        await page.fill("#search-form-input", url)

        print("✅ Clicking download...")
        await page.click("#app > section.form-block > div > form > button")

        print("⏳ Waiting for link...")
        await page.wait_for_timeout(10000)  # wait for JS

        try:
            await page.wait_for_selector("#app > div.search-result.show > div > div > ul.output-list__list.output-list__list--one-item > li > div.media-content__info > a", timeout=50000)
            
            download_element = await page.query_selector("#app > div.search-result.show > div > div > ul.output-list__list.output-list__list--one-item > li > div.media-content__info > a")
            download_url = await download_element.get_attribute("href")
            print("✅ Got link, wait at least 2 min !")
        except Exception as e:
            print("❌ Error:", e)
            await page.screenshot(path="debug.png")
            html = await page.content()
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            download_url = None

        await browser.close()
        return download_url
    
# ✅ WRAPPER
def reel_sync(url: str) -> str:
    return asyncio.run(reel(url))

