from typing import Dict, List


def generate_storyboard(script: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Convert script into a 5-shot storyboard.
    """
    return [
        {
            "shot": "1",
            "visual": "近景：主角突然停下动作，盯着手机或现场异常细节。",
            "voice": script.get("opening", "")[:80] + "……",
            "duration": "5s",
            "camera": "快速推近，制造压迫感。",
        },
        {
            "shot": "2",
            "visual": "中景：主角尝试确认异常来源，环境开始出现不对劲的变化。",
            "voice": "主角：这不可能，刚才明明不是这样。",
            "duration": "6s",
            "camera": "手持轻微晃动，增强真实感。",
        },
        {
            "shot": "3",
            "visual": "特写：关键线索出现，例如纸条、屏幕提示、人物表情变化。",
            "voice": script.get("conflict", "")[:80] + "……",
            "duration": "7s",
            "camera": "特写停留 1 秒，再快速切走。",
        },
        {
            "shot": "4",
            "visual": "远景：主角陷入选择，周围人物或环境形成压迫。",
            "voice": "旁白：他现在只有一次选择机会。",
            "duration": "6s",
            "camera": "横移跟拍，突出紧张节奏。",
        },
        {
            "shot": "5",
            "visual": "反转镜头：主角回头发现真正的问题才刚刚开始。",
            "voice": script.get("ending", "")[:90] + "……",
            "duration": "6s",
            "camera": "慢推 + 戛然而止，留下悬念。",
        },
    ]
