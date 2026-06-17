from typing import Dict


def generate_script(topic: Dict[str, str]) -> Dict[str, str]:
    """
    Generate a simple three-act script from selected topic.
    """
    title = topic.get("title", "未命名选题")
    hook = topic.get("hook", "强冲突开场")

    return {
        "opening": f"【开场】主角遇到一个和「{title}」有关的异常事件。镜头快速切入冲突，用一句反常识台词制造悬念：为什么事情会变成这样？",
        "conflict": f"【冲突】主角尝试解决问题，却发现规则越来越复杂。围绕“{hook}”持续升级矛盾，让观众产生继续观看的理由。",
        "ending": "【结尾】主角以为问题解决，最后一个细节揭示更大的危机，为下一集或评论区讨论留下钩子。",
    }
