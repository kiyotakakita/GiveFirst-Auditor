# src/collector.py
import os
import requests
from src.sheets import get_sheet_client

def search_web_signals(query: str, limit: int = 5) -> list:
    """
    抽象化されたシグナル収集（例: DuckDuckGoや無料検索APIを利用）
    『〇〇 困った』などの悩みの声をWeb上から収集してURLを返す
    """
    print(f"📡 シグナル探索中: '{query}'")
    # ここにXのAPIや、Web検索、note検索などを差し込む
    # 今回は例として検索で見つかったURLリストを返すモック
    found_urls = [
        # 実際はAPI等で取得したURLがここに入る
    ]
    return found_urls

def append_urls_to_sheet(sheet_id: str, urls: list):
    """見つかったURLをスプレッドシートのA列（未処理）に自動追記"""
    if not urls:
        print("新しいシグナルは見つかりませんでした。")
        return

    worksheet = get_sheet_client(sheet_id)
    # 追記する行データを作成: [URL, "PENDING"]
    rows_to_add = [[url, "PENDING"] for url in urls]
    worksheet.append_rows(rows_to_add)
    print(f"📥 {len(rows_to_add)} 件の新規ターゲットをスプレッドシートに追記しました。")

if __name__ == "__main__":
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
    # 抽象化された探索キーワード
    SEARCH_QUERY = "社内 AI 導入 課題 困った"
    
    urls = search_web_signals(SEARCH_QUERY)
    append_urls_to_sheet(SPREADSHEET_ID, urls)
