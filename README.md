コンテキスト認識型リード適格性・摩擦監査エンジン
# GiveFirst-Auditor 🛡️🤝

> **「コピペ絨毯爆撃」を撲滅し、敬意ある先行ギブと適切な出会いだけを自動化する監査エンジン**

営業やアライアンスのアプローチにおいて、「相手の文脈を読まない定型文DMを送って炎上・晒される事故」を未然に防ぎ、自社の提供価値が**「今まさに救いになる相手」**だけを安全に抽出・アドバイスするシステムです。

---

## 💡 特徴

1. **ノーコード運用（スプレッドシート連携）**
   営業担当者は、気になる相手のnote・X・WebサイトのURLをスプレッドシートのA列に貼るだけ。裏でGitHub Actionsが巡回し、数分でB〜F列に判定を書き込みます。
2. **商材を選ばない汎用性（完全抽象化）**
   `config.yaml` を書き換えるだけで、AI導入支援、SEO、Web受託、採用スカウトなど、あらゆる業界の判定ルールに対応。
3. **炎上・被曝ガードレール**
   相手が業界のトップ有識者や研究者の場合、自動で `DANGER`（接触禁止）ラベルを付与し、ブランド毀損を防止。
4. **マインドセット李さん流「先行ギブ」の生成**
   アポをねだるのではなく、「相手の課題に寄り添った情報提供・お役立ち資料」の切り口を自動生成。

---

## 📋 スプレッドシートのレイアウト

スプレッドシートの1行目に以下のヘッダーを作成してください：

| A列: URL | B列: Status | C列: Risk Label | D列: Level Gap | E列: Action | F列: Reason & Advice |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `https://note.com/...` | *(自動)* | `DANGER` / `SAFE` | `TOO_HIGH` 等 | `GIVE_FIRST` 等 | 具体的な助言 |

---

## 🚀 セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://github.com/your-username/GiveFirst-Auditor.git
cd GiveFirst-Auditor
pip install -r requirements.txt
```

### 2. Google Cloud サービスアカウントの発行
1. Google Cloud Console でサービスアカウントを作成し、キー（JSON）をダウンロード。
2. 連携したいスプレッドシートの「共有」に、サービスアカウントのメールアドレスを**編集者**として追加。
3. スプレッドシートのURLからID（`https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`）を控える。

### 3. GitHub Secrets の登録
リポジトリの **Settings > Secrets and variables > Actions** に以下を登録：

| Secret名 | 内容 |
| :--- | :--- |
| `OPENAI_API_KEY` | OpenAIのAPIキー |
| `SPREADSHEET_ID` | スプレッドシートのID |
| `GCP_SERVICE_ACCOUNT_JSON` | ダウンロードしたJSONファイルの中身をそのまま貼り付け |

### 4. 設定のカスタマイズ
`config.yaml` を開き、自社の商材・提供できる価値（Can）・避けるべき相手を記載してコミットします。
