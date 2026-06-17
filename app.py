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
        background: linear-gradient(180deg, #f6f8fb 0%, #eef2f7 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1180px;
    }
    .hero-card {
        padding: 30px 34px;
        border-radius: 24px;
        background: linear-gradient(135deg, #111827 0%, #1f2937 56%, #374151 100%);
        color: white;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
        margin-bottom: 22px;
    }
    .hero-kicker {
        font-size: 13px;
        letter-spacing: 0.16em;
        color: #c7d2fe;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 38px;
        font-weight: 850;
        line-height: 1.18;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #e5e7eb;
        line-height: 1.75;
        max-width: 840px;
        margin-bottom: 18px;
    }
    .tag {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        margin: 0 8px 8px 0;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #f9fafb;
        font-size: 13px;
        font-weight: 600;
    }
    .mode-box {
        margin-top: 12px;
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.16);
        color: #f3f4f6;
        font-size: 14px;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        min-height: 106px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }
    .metric-title {
        color: #6b7280;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #111827;
        font-size: 17px;
        font-weight: 800;
        line-height: 1.45;
    }
    .section-title {
        margin-top: 24px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .step-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: #111827;
        color: #ffffff;
        font-size: 12px;
        font-weight: 800;
    }
    .section-heading {
        font-size: 22px;
        font-weight: 850;
        color: #111827;
    }
    .muted {
        color: #6b7280;
        font-size: 14px;
        line-height: 1.65;
    }
    .selected-topic {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 14px;
        margin-top: 12px;
    }
    .history-panel {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        margin-top: 24px;
    }
    .value-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        min-height: 150px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }
    .value-card h4 {
        margin: 0 0 10px 0;
        color: #111827;
    }
    .value-card p {
        margin: 0;
        color: #4b5563;
        line-height: 1.65;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_section_title(step: str, title: str) -> None:
    st.markdown(
        f"""
        <div class="section-title">
            <span class="step-pill">{step}</span>
            <span class="section-heading">{title}</span>
        </div>
        """,
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
            <h4>{title}</h4>
            <p>{body}</p>
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
    <div class="hero-card">
        <div class="hero-kicker">AI CONTENT WORKFLOW MVP</div>
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
            当前模式：Mock 数据演示版。后续可接入 Claude / OpenAI / DeepSeek 等大模型 API。
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
            '<div class="muted">输入一个内容方向，生成适合继续策划的短剧/短视频选题。</div>',
            unsafe_allow_html=True,
        )
        theme = st.text_input(
            "主题",
            placeholder="例如：末日求生、山海经怪谈、未来科幻、都市反转",
            label_visibility="collapsed",
        )

        if st.button("生成选题", type="primary", use_container_width=True):
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
                        use_container_width=True,
                        type="primary" if is_selected else "secondary",
                    ):
                        st.session_state.selected_topic_index = index
                        st.session_state.selected_topic = topic
                        st.session_state.script = None
                        st.session_state.storyboard = None
                        st.rerun()

        selected_topic = st.session_state.selected_topic
        if selected_topic:
            st.markdown(
                f"""
                <div class="selected-topic">
                    <b>已选选题：</b>{selected_topic['title']}<br>
                    <span>{selected_topic['summary']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button(
            "生成脚本",
            use_container_width=True,
            disabled=not bool(selected_topic),
        ):
            st.session_state.script = generate_script(st.session_state.selected_topic)
            st.session_state.storyboard = None
            st.success("脚本已生成。")

    render_section_title("Step 3", "生成分镜表并导出方案")

    if st.session_state.script:
        st.markdown(
            '<div class="muted">脚本按开场、冲突、结尾拆分，方便快速评审和继续生成分镜。</div>',
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
            '<div class="muted">把脚本拆解为镜头编号、画面描述、台词/旁白、时长和运镜建议。</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "生成分镜表",
            use_container_width=True,
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
                use_container_width=True,
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
                use_container_width=True,
            )


with history_col:
    st.markdown('<div class="history-panel">', unsafe_allow_html=True)
    st.markdown("### 历史记录")
    st.markdown(
        '<div class="muted">生成分镜后自动保存，便于恢复最近方案。</div>',
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

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("## 项目价值")
st.markdown(
    '<div class="muted">这个 MVP 重点展示如何把内容生产中的重复整理工作，拆解成可操作、可导出、可复用的工具流程。</div>',
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
