import requests
import json
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scrapers.base import BaseClient
from playwright.sync_api import sync_playwright

# #region agent log helper
def _dbg(hyp, msg, data): open('/app/.cursor/debug.log','a').write(json.dumps({"hypothesisId":hyp,"message":msg,"data":data,"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
# #endregion

"""HTTP client for making requests to HLTV.org with rate limiting and error handling."""
class HLTVClient(BaseClient):
    def __init__(self):
        self.base_url = "https://www.hltv.org/stats/"

    def get_top_50_teams(self):
        current_date = datetime.now()
        last_three_months = current_date - relativedelta(months=3)
        with sync_playwright() as p:
            # #region agent log - try Firefox with stealth JS injection (Hypothesis G, F, H)
            _dbg("G", "using_firefox", {"browser": "firefox"})
            browser = p.firefox.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
                viewport={'width': 1920, 'height': 1080},
            )
            page = context.new_page()
            
            # Inject script to mask webdriver detection (Hypothesis F)
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = { runtime: {} };
            """)
            _dbg("F", "stealth_js_injected", {"properties": ["webdriver", "plugins", "languages", "chrome"]})
            # #endregion
            
            url = self.base_url + "teams?startDate=" + last_three_months.strftime("%Y-%m-%d") + "&endDate=" + current_date.strftime("%Y-%m-%d") + "&rankingFilter=Top50"

            page.goto(url, timeout=60000, wait_until='domcontentloaded')

            # #region agent log - wait for Cloudflare to resolve
            _dbg("FIX", "initial_title", {"title": page.title()})
            
            # Wait for Cloudflare challenge to resolve (title changes from "Just a moment...")
            for i in range(30):  # Try for 30 seconds
                if "just a moment" not in page.title().lower():
                    _dbg("FIX", "cloudflare_passed", {"attempt": i, "title": page.title()})
                    break
                _dbg("FIX", "waiting_cloudflare", {"attempt": i, "title": page.title()})
                page.wait_for_timeout(1000)
            # #endregion

            # #region agent log - after navigation
            _dbg("D", "page_url_after_nav", {"url": page.url})
            _dbg("A,E", "page_title", {"title": page.title()})
            _dbg("A,E", "page_html_snippet", {"html": page.content()[:2000]})
            _dbg("B", "all_tables_on_page", {"tables": [t.get_attribute("class") for t in page.query_selector_all("table")]})
            _dbg("E", "cloudflare_check", {"has_cf": "cloudflare" in page.content().lower() or "challenge" in page.content().lower()})
            # #endregion

            print(page)

            page.wait_for_selector("table.stats-table.player-ratings-table", timeout=60000)

            teams = page.query_selector_all("table.stats-table.player-ratings-table tbody tr")

            for row in teams:
                name = row.query_selector("td.teamCol-teams-overview").inner_text()
                print(name)

            browser.close()

client = HLTVClient()
print(client.get_top_50_teams())