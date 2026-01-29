import asyncio
import random
import nodriver as uc


START_DATE = "2026-01-20"
END_DATE = "2026-01-26"


def random_delay(min_sec=0.5, max_sec=1.5):
    return random.uniform(min_sec, max_sec)


async def scraper():
    # Launch undetected Chrome
    browser = await uc.start()
    
    # Open HLTV results page
    page = await browser.get("https://www.hltv.org/results")
    await page
    await asyncio.sleep(random_delay(3, 5))
    
    # 1️⃣ Double-click start date input to open calendar
    start_input = await page.select('input[name="startDate"]')
    if start_input:
        await start_input.click()
        await asyncio.sleep(0.2)
        await start_input.click()
        print("Opened calendar")
    await asyncio.sleep(random_delay(1, 2))
    
    # 2️⃣ Click the start date in calendar
    start_day = START_DATE.split('-')[2].lstrip('0')  # "20"
    days = await page.select_all('.day')
    print(f"Found {len(days)} day elements")
    
    for day in days:
        try:
            text = day.text
            if text and text.strip() == start_day:
                await day.click()
                print(f"Selected start date: {START_DATE}")
                break
        except:
            continue
    await asyncio.sleep(random_delay(0.8, 1.5))
    
    # 3️⃣ Click the end date in calendar
    end_day = END_DATE.split('-')[2].lstrip('0')  # "26"
    days = await page.select_all('.day')
    
    for day in days:
        try:
            text = day.text
            if text and text.strip() == end_day:
                await day.click()
                print(f"Selected end date: {END_DATE}")
                break
        except:
            continue
    await asyncio.sleep(random_delay(1, 2))
    
    # Wait for results to load after date selection
    print("Waiting for results to load...")
    await asyncio.sleep(random_delay(8, 12))
    
    await page
    print(f"Done! URL: {page.url}")
    
    # Save HTML content
    html = await page.get_content()
    with open("hltv_results.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved HTML to hltv_results.html")
    
    input("Press Enter to close...")
    browser.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(scraper())
