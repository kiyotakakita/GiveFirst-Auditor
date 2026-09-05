import os
import yaml
from openai import OpenAI
from src.fetcher import extract_text_from_url
from src.auditor import evaluate_lead
from src.sheets import get_sheet_client

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_pipeline():
    config = load_config()
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    sheet_id = os.environ["SPREADSHEET_ID"]
    worksheet = get_sheet_client(sheet_id)

    # 全行取得（1行目はヘッダー想定）
    # カラム構成想定:
    # A: URL | B: ステータス(PENDING/DONE) | C: 判定(SAFE/DANGER) | D: ギャップ | E: アクション | F: アドバイス
    records = worksheet.get_all_values()
    if len(records) <= 1:
        print("処理対象データがありません。")
        return

    print(f"監査パイプライン開始: 合計 {len(records)-1} 件のデータを確認中...")

    for idx, row in enumerate(records[1:], start=2):
        url = row[0].strip() if len(row) > 0 else ""
        status = row[1].strip() if len(row) > 1 else ""

        # 未処理行（URLがあり、B列がDONEでない）のみ実行
        if url and status != "DONE":
            print(f"[{idx}行目を処理中] URL: {url}")
            text = extract_text_from_url(url)
            
            if not text:
                worksheet.update(values=[["ERROR", "SKIP", "N/A", "N/A", "テキスト取得失敗"]], range_name=f"B{idx}:F{idx}")
                continue

            audit = evaluate_lead(client, config, url, text)

            # 結果をスプレッドシートに書き込み
            update_data = [
                "DONE",
                audit.risk_label,
                audit.level_gap,
                audit.action_type,
                f"【理由】{audit.reason}\n【助言】{audit.advice}"
            ]
            worksheet.update(values=[update_data], range_name=f"B{idx}:F{idx}")
            print(f" -> 結果: [{audit.risk_label}] アクション: [{audit.action_type}]")

    print("全処理が完了しました。")

if __name__ == "__main__":
    run_pipeline()
