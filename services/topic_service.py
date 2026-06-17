from typing import List, Dict


def generate_topics(theme: str) -> List[Dict[str, str]]:
    """
    Mock topic generation.
    后续可替换为真实大模型 API 调用。
    """
    theme = theme.strip() or "短视频选题"

    return [
        {
            "title": f"《{theme}：第一分钟就反转》",
            "summary": f"围绕“{theme}”设计一个强钩子短剧，前 10 秒制造悬念，中段不断加压，结尾反转。",
            "hook": "开头直接给冲突，结尾强反转，适合提升完播率。",
            "platform": "抖音 / 快手 / 视频号",
        },
        {
            "title": f"《如果{theme}发生在普通人身上》",
            "summary": f"把“{theme}”落到普通人的日常选择中，用代入感带动情绪共鸣。",
            "hook": "普通人视角、低成本拍摄、容易引发评论讨论。",
            "platform": "抖音 / 小红书 / B站短视频",
        },
        {
            "title": f"《{theme}背后的隐藏规则》",
            "summary": f"用解密式结构讲述“{theme}”背后的规则、风险和选择。",
            "hook": "信息差 + 悬念推进，适合做系列化内容。",
            "platform": "B站 / 抖音 / 视频号",
        },
    ]
