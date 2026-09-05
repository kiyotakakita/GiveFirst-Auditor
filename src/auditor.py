import json
from pydantic import BaseModel, Field
from typing import Literal
from openai import OpenAI

class AuditResult(BaseModel):
    risk_label: Literal["SAFE", "DANGER", "SKIP"] = Field(description="安全/炎上リスク/対象外")
    level_gap: Literal["PROSPECT_TOO_HIGH", "JUST_FIT", "PROSPECT_TOO_LOW"]
    action_type: Literal["GIVE_FIRST", "DO_NOT_CONTACT", "SOLVE_PAIN"]
    reason: str = Field(description="なぜこの判定になったのかの簡潔な理由")
    advice: str = Field(description="李さん流の先行ギブ文面案、または接触禁止の理由")

def evaluate_lead(client: OpenAI, config: dict, target_url: str, target_text: str) -> AuditResult:
    service = config["service"]
    criteria = config["criteria"]

    prompt = f"""
    あなたは「コンテキスト認識型アプローチ監査AI」です。
    相手のWeb公開情報（記事、SNS、ブログ等）を読み、自社の提案が相手に届いた時の「適合度」と「摩擦・炎上リスク」を判定してください。
    マインドセット李さんの人脈術のように、「相手の文脈を尊重し、不要な売り込みをせず、価値を先行ギブできるか」を最重要視します。

    【自社の提供価値】
    - サービス名: {service['name']}
    - ターゲット層: {service['target_maturity']}
    - 提供できる価値: {service['core_value']}
    - 絶対に売ってはいけない相手（アンチターゲット）: {', '.join(service['anti_targets'])}

    【判定基準】
    - DANGER基準: {criteria['danger_definition']}
    - SAFE基準: {criteria['safe_definition']}

    【対象者の公開情報】
    URL: {target_url}
    内容抜粋:
    {target_text[:2000]}

    以下のスキーマに準拠してJSONで判定を出力してください。
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=AuditResult,
        temperature=0.2
    )
    return response.choices[0].message.parsed
