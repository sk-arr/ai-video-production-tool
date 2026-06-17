"""
Prompt templates for future real AI model integration.
当前 MVP 默认使用 Mock 数据，后续可以把这些模板交给 Claude / OpenAI / DeepSeek 等模型。
"""

TOPIC_PROMPT = """
你是短剧/短视频策划。请围绕主题「{theme}」生成 3 个适合短视频或短剧的选题。
每个选题包含：标题、简介、爆点、适合平台。
输出 JSON 数组。
"""

SCRIPT_PROMPT = """
你是短剧编剧。请基于选题「{title}」生成三段式脚本。
结构包含：开场、冲突、结尾。要求节奏快、冲突明确、适合短视频。
输出 JSON。
"""

STORYBOARD_PROMPT = """
你是短视频分镜师。请把脚本拆成 5 个镜头。
每个镜头包含：镜头编号、画面描述、台词/旁白、时长、运镜建议。
输出 JSON 数组。
"""
