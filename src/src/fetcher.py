import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str, timeout: int = 10) -> str:
    """URLからメインテキストを自動抽出（スクレイピング）"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GiveFirstAuditor/1.0"}
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)
        return text
    except Exception as e:
        print(f"[Fetcher Error] {url}: {e}")
        return ""
