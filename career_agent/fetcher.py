from typing import Optional
import requests
from .config import AgentConfig

def headers(cfg: AgentConfig):
    return {"User-Agent": cfg.user_agent, "Accept-Language": "en-US,en;q=0.9,he-IL;q=0.8"}

def fetch(url: str, cfg: AgentConfig) -> Optional[str]:
    try:
        r = requests.get(url, headers=headers(cfg), timeout=cfg.request_timeout_sec)
        if r.status_code == 200:
            return r.text
        return None
    except Exception:
        return None

# Optional Selenium fallback
def fetch_selenium(url: str, cfg: AgentConfig) -> Optional[str]:
    if not cfg.selenium_enabled:
        return None
    try:
        import time
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        opts = Options()
        if cfg.selenium_headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--window-size=1600,1200")
        opts.add_argument(f"user-agent={cfg.user_agent}")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
        try:
            driver.set_page_load_timeout(cfg.request_timeout_sec)
            driver.get(url)
            time.sleep(3.0)
            return driver.page_source
        finally:
            driver.quit()
    except Exception:
        return None
