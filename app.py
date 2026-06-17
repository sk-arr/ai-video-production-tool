import streamlit as st

from services.topic_service import generate_topics
from services.script_service import generate_script
from services.storyboard_service import generate_storyboard, format_storyboard_for_display
from utils.storage import save_record, load_history, build_markdown


st.set_page_config(
    page_title="AI短剧/短视频生产效率工具",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(45, 212, 191, 0.15), transparent 30rem),
            radial-gradient(circle at 92% 12%, rgba(59, 130, 246, 0.10), transparent 28rem),
            linear-gradient(135deg, #f8fafc 0%, #eef2f7 52%, #f8fafc 100%);
    }
    .block-container {
        max-width: 1220px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f172a;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] li {
        color: #475569;
        font-size: 14px;
        line-height: 1.65;
    }
    .hero {
        border: 1px solid rgba(203, 213, 225, 0.78);
        border-radius: 20px;
        padding: 34px 36px;
        background: rgba(255, 255, 255, 0.88);
        box-shadow: 0 20px 48px rgba(15, 23, 42, 0.08);
        margin-bottom: 18px;
    }
    .hero-eyebrow {
        color: #0f766e;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .hero-title {
        color: #0f172a;
        font-size: 38px;
        font-weight: 850;
        line-height: 1.18;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        color: #475569;
        font-size: 17px;
        line-height: 1.7;
        max-width: 820px;
        margin-bottom: 18px;
    }
    .tag {
        display: inline-block;
        padding: 6px 12px;
        border: 1px solid #dbe4ef;
        border-radius: 999px;
        background: #f8fafc;
        color: #334155;
        font-size: 13px;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .mode-box {
        margin-top: 14px;
        border: 1px solid #99f6e4;
        border-radius: 12px;
        background: #f0fdfa;
        color: #115e59;
        padding: 12px 14px;
        font-size: 14px;
        line-height: 1.55;
    }
    .metric-card {
        border: 1px solid rgba(203, 213, 225, 0.82);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.86);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.055);
        padding: 17px 18px;
        min-height: 112px;
        margin-bottom: 16px;
    }
    .metric-title {
        color: #0f766e;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 9px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 17px;
        font-weight: 780;
        line-height: 1.45;
    }
    .section-title {
        color: #0f172a;
        font-size: 22px;
        font-weight: 840;
        margin: 18px 0 10px 0;
    }
    .step-badge {
        display: inline-block;
        color: #ffffff;
        background: #0f172a;
        border-radius: 999px;
        padding: 4px 10px;
        margin-right: 8px;
        font-size: 12px;
        font-weight: 780;
    }
    .section-note {
        color: #64748b;
        font-size: 14px;
        line-height: 1.65;
        margin-bottom: 12px;
    }
    .selected-topic {
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        background: #eff6ff;
        color: #1e3a8a;
        padding: 12px 14px;
        margin: 12px 0;
        font-size: 14px;
        line-height: 1.6;
    }
    .history-card {
        border: 1px solid rgba(203, 213, 225, 0.82);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.86);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.055);
        padding: 18px;
        margin-top: 18px;
    }
    .history-title {
        color: #0f172a;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .history-desc {
        color: #64748b;
        font-size: 13px;
        line-height: 1.55;
        margin-bottom: 10px;
    }
    .value-section {
        margin-top: 28px;
        border: 1px solid rgba(203, 213, 225, 0.82);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.88);
        box-shadow: 0 20px 48px rgba(15, 23, 42, 0.07);
        padding: 24px 26px;
    }
    .value-title {
        color: #0f172a;
        font-size: 24px;
        font-weight: 850;
        margin-bottom: 8px;
    }
    .value-subtitle {
        color: #64748b;
        font-size: 14px;
        line-height: 1.65;
        margin-bottom: 14px;
    }
    .value-card {
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        background: #f8fafc;
        min-height: 145px;
        padding: 16px;
        color: #334155;
    }
    .value-card-title {
        color: #0f172a;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .value-card-body {
        color: #475569;
        font-size: 14px;
        line-height: 1.62;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(203, 213, 225, 0.86);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.88);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.055);
    }
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 700;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_section_title(step: str, title: str) -> None:
    st.markdown(
        f'<div class="section-title"><span class="step-badge">{step}</span>{title}</div>',
        unsafe_allow_html=True,
    )


def render_metric_card(title: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_value_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="value-card">
            <div class="value-card-title">{title}</div>
            <div class="value-card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("## 项目说明")
    st.markdown("### 项目定位")
    st.write("AI辅助短剧/短视频生产效率工具")

    st.markdown("### 适合场景")
    st.markdown(
        """
        - 短剧选题策划
        - 短视频脚本生成
        - 分镜拆解
        - 团队内容协作
        - 面试项目演示
        """
    )

    st.markdown("### 技术栈")
    st.markdown(
        """
        - Python
        - Streamlit
        - JSON
        - Prompt 模板
        - GitHub
        - Streamlit Cloud
        """
    )

    st.markdown("### 当前版本说明")
    st.write("当前版本为 Mock 演示版，主要展示业务流程拆解、工具搭建和结构化输出能力。")


st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">AI CONTENT WORKFLOW MVP</div>
        <div class="hero-title">AI短剧/短视频生产效率工具</div>
        <div class="hero-subtitle">
            输入一个主题，快速生成选题、脚本和分镜方案，帮助短剧/短视频团队减少重复整理工作。
        </div>
        <span class="tag">AI辅助开发</span>
        <span class="tag">短剧策划</span>
        <span class="tag">脚本生成</span>
        <span class="tag">分镜拆解</span>
        <span class="tag">Markdown导出</span>
        <span class="tag">可演示MVP</span>
        <div class="mode-box">
            当前模式：Mock 数据演示版<br>
            后续可接入 Claude / OpenAI / DeepSeek 等大模型 API
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_columns = st.columns(4)
metrics = [
    ("完整流程", "主题 → 选题 → 脚本 → 分镜"),
    ("结构化输出", "支持 Markdown 导出"),
    ("业务场景", "短剧 / 短视频内容生产"),
    ("扩展能力", "可接入真实大模型 API"),
]
for column, (title, value) in zip(metric_columns, metrics):
    with column:
        render_metric_card(title, value)

if "topics" not in st.session_state:
    st.session_state.topics = []
if "selected_topic_index" not in st.session_state:
    st.session_state.selected_topic_index = None
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None
if "script" not in st.session_state:
    st.session_state.script = None
if "storyboard" not in st.session_state:
    st.session_state.storyboard = None


main_col, history_col = st.columns([2.35, 0.95], gap="large")

with main_col:
    render_section_title("Step 1", "输入主题并生成选题")
    with st.container(border=True):
        st.markdown("#### 内容主题")
        st.markdown(
            '<div class="section-note">输入一个内容方向，生成适合继续策划的短剧/短视频选题。</div>',
            unsafe_allow_html=True,
        )
        theme = st.text_input(
            "主题",
            placeholder="例如：末日求生、山海经怪谈、未来科幻、都市反转",
            label_visibility="collapsed",
        )

        if st.button("生成选题", type="primary", width="stretch"):
            st.session_state.topics = generate_topics(theme)
            st.session_state.selected_topic_index = None
            st.session_state.selected_topic = None
            st.session_state.script = None
            st.session_state.storyboard = None
            st.success("已生成 3 个选题。")

    render_section_title("Step 2", "选择选题并生成脚本")

    if not st.session_state.topics:
        st.info("先在 Step 1 生成选题，再选择一个方向继续生成脚本。")
    else:
        topic_columns = st.columns(3)
        for index, topic in enumerate(st.session_state.topics):
            with topic_columns[index % 3]:
                with st.container(border=True):
                    st.markdown(f"#### {topic['title']}")
                    st.markdown("**简介**")
                    st.write(topic["summary"])
                    st.markdown(f"**爆点：** {topic['hook']}")
                    st.markdown(f"**适合平台：** {topic['platform']}")

                    is_selected = st.session_state.selected_topic_index == index
                    if is_selected:
                        st.success("当前选择")

                    if st.button(
                        "选择这个选题",
                        key=f"select_topic_{index}",
                        width="stretch",
                        type="primary" if is_selected else "secondary",
                    ):
                        st.session_state.selected_topic_index = index
                        st.session_state.selected_topic = topic
                        st.session_state.script = None
                        st.session_state.storyboard = None

        selected_topic = st.session_state.selected_topic
        if selected_topic:
            st.markdown(
                f"""
                <div class="selected-topic">
                    <strong>已选选题：</strong>{selected_topic['title']}<br>
                    {selected_topic['summary']}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button(
            "生成脚本",
            width="stretch",
            disabled=not bool(selected_topic),
        ):
            st.session_state.script = generate_script(st.session_state.selected_topic)
            st.session_state.storyboard = None
            st.success("脚本已生成。")

    render_section_title("Step 3", "生成分镜表并导出方案")

    if st.session_state.script:
        st.markdown(
            '<div class="section-note">脚本按开场、冲突、结尾拆分，方便快速评审和继续生成分镜。</div>',
            unsafe_allow_html=True,
        )
        script = st.session_state.script
        script_columns = st.columns(3)
        for column, (label, content) in zip(
            script_columns,
            [
                ("开场", script["opening"]),
                ("冲突", script["conflict"]),
                ("结尾", script["ending"]),
            ],
        ):
            with column:
                with st.container(border=True):
                    st.markdown(f"#### {label}")
                    st.write(content)
    else:
        st.info("生成脚本后，这里会展示三段式脚本和分镜生成入口。")

    with st.container(border=True):
        st.markdown("#### 分镜表")
        st.markdown(
            '<div class="section-note">把脚本拆解为镜头编号、画面描述、台词/旁白、时长和运镜建议。</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "生成分镜表",
            width="stretch",
            disabled=not bool(st.session_state.script),
        ):
            st.session_state.storyboard = generate_storyboard(st.session_state.script)
            record = {
                "theme": theme.strip() or "短视频选题",
                "topic": st.session_state.selected_topic,
                "script": st.session_state.script,
                "storyboard": st.session_state.storyboard,
            }
            save_record(record)
            st.success("分镜表已生成，并保存到历史记录。")

        if st.session_state.storyboard:
            st.dataframe(
                format_storyboard_for_display(st.session_state.storyboard),
                width="stretch",
                hide_index=True,
            )

            record = {
                "theme": theme.strip() or "短视频选题",
                "topic": st.session_state.selected_topic,
                "script": st.session_state.script,
                "storyboard": st.session_state.storyboard,
            }
            markdown = build_markdown(record)

            st.download_button(
                "导出 Markdown 方案",
                data=markdown,
                file_name="ai_video_plan.md",
                mime="text/markdown",
                width="stretch",
            )

with history_col:
    st.markdown(
        """
        <div class="history-card">
            <div class="history-title">历史记录</div>
            <div class="history-desc">生成分镜后自动保存，便于恢复最近方案。</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    history = load_history()

    if not history:
        st.info("还没有历史记录。")
    else:
        for index, item in enumerate(history[:5]):
            topic = item.get("topic", {})
            title = topic.get("title", "未命名方案")
            with st.expander(title):
                st.caption(item.get("created_at", ""))
                st.markdown(f"**选题标题：** {title}")
                st.write(topic.get("summary", ""))
                if st.button("恢复这个方案", key=f"restore_{index}_{item.get('created_at', '')}"):
                    st.session_state.topics = [topic] if topic else []
                    st.session_state.selected_topic_index = 0 if topic else None
                    st.session_state.selected_topic = topic
                    st.session_state.script = item.get("script")
                    st.session_state.storyboard = item.get("storyboard")
                    st.rerun()

st.markdown(
    """
    <div class="value-section">
        <div class="value-title">项目价值</div>
        <div class="value-subtitle">
            这个 MVP 重点展示如何把内容生产中的重复整理工作，拆解成可操作、可导出、可复用的工具流程。
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

value_columns = st.columns(4)
value_cards = [
    (
        "业务痛点",
        "短剧/短视频生产中，选题、脚本、分镜整理重复度高，人工整理成本较大。",
    ),
    (
        "解决方案",
        "将内容生产流程拆解为工具流程，实现主题输入、选题生成、脚本生成、分镜输出。",
    ),
    (
        "团队复用",
        "输出结构化内容，便于复制、导出、复用和团队协作。",
    ),
    (
        "后续扩展",
        "后续可接入 Claude、OpenAI、DeepSeek 等大模型 API，并增加 Prompt 模板管理和成本统计。",
    ),
]
for column, (title, body) in zip(value_columns, value_cards):
    with column:
        render_value_card(title, body)
