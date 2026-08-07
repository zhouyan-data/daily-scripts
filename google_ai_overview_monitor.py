# 监控品牌在 Google AI Overview 里的出现情况
# 来源：https://www.cnblogs.com/A381532662/p/22321380

import requests

API = "https://api.serpbase.dev"
KEY = "你的key"  # 需要注册获取

def check_ai_overview(query, brand):
    """
    检查指定关键词的 AI Overview 情况
    
    Args:
        query: 搜索关键词
        brand: 品牌名称
    
    Returns:
        dict: 包含 AI Overview 出现情况、品牌提及、organic 排名等信息
    """
    r = requests.post(
        f"{API}/google/search",
        headers={"X-API-Key": KEY},
        json={"q": query, "hl": "en", "gl": "us"},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    
    return {
        "query": query,
        "has_ai_overview": bool(data.get("ai_overview")),
        "mentions_brand": brand.lower() in (data.get("ai_overview", {}).get("text", "") or "").lower(),
        "top_organic_rank": (data.get("organic") or [{}])[0].get("rank"),
        "request_id": data.get("request_id"),
    }

if __name__ == "__main__":
    # 使用示例
    result = check_ai_overview("best serp api 2026", "yourbrand")
    print(result)
