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
    .block-container { padding-top: 2rem; padding-bottom: 2.5rem; max-width: 1180px; }
    .hero {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px 26px;
        background: #ffffff;
        margin-bottom: 22px;
    }
    .hero-title { font-size: 34px; font-weight: 800; margin-bottom: 8px; color: #111827; }
    .hero-position { color: #4b5563; font-size: 16px; margin-bottom: 18px; line-height: 1.65; }
    .tag {
        display: inline-block;
        padding: 5px 11px;
        border: 1px solid #d1d5db;
        border-radius: 999px;
        margin-right: 8px;
        margin-bottom: 8px;
        color: #374151;
        font-size: 13px;
        background: #f9fafb;
    }
    .mode-box {
        border-left: 4px solid #0f766e;
        padding: 10px 14px;
        background: #f0fdfa;
        color: #134e4a;
        border-radius: 6px;
        margin-top: 14px;
        font-size: 14px;
    }
    .scenario {
        color: #4b5563;
        font-size: 14px;
        margin-top: 10px;
    }
    .step-heading {
        font-size: 20px;
        font-weight: 750;
        color: #111827;
        margin: 16px 0 10px 0;
    }
    .step-kicker {
        display: inline-block;
        margin-right: 8px;
        padding: 3px 9px;
        border-radius: 999px;
        background: #111827;
        color: #ffffff;
        font-size: 12px;
    }
    .section-note { color: #6b7280; font-size: 14px; margin-bottom: 10px; }
    div[data-testid="stButton"] > button { border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">AI 短剧 / 短视频生产效率工具</div>
        <div class="hero-position">
            面向内容团队的轻量 MVP：把“主题输入、选题策划、脚本生成、分镜拆解、方案导出”
            串成一个可演示的结构化工作流。
        </div>
        <span class="tag">AI 工具开发</span>
        <span class="tag">短剧策划</span>
        <span class="tag">短视频脚本</span>
        <span class="tag">分镜拆解</span>
        <span class="tag">Markdown 导出</span>
        <div class="mode-box">当前模式：Mock 数据 / 后续可接入真实大模型 API</div>
        <div class="scenario">适合场景：短剧策划、短视频脚本、分镜拆解、团队内容协作</div>
    </div>
    """,
    unsafe_allow_html=True,
)

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


left, right = st.columns([2, 1])

with left:
    st.markdown(
        '<div class="step-heading"><span class="step-kicker">第一步</span>输入主题并生成选题</div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        theme = st.text_input(
            "内容主题",
            placeholder="例如：末日求生、山海经怪谈、未来科幻、都市反转",
        )
        st.caption("输入一个内容方向，系统会生成 3 个可继续深化的短剧/短视频选题。")

        if st.button("生成选题", type="primary", use_container_width=True):
            st.session_state.topics = generate_topics(theme)
            st.session_state.selected_topic_index = None
            st.session_state.selected_topic = None
            st.session_state.script = None
            st.session_state.storyboard = None
            st.success("已生成 3 个选题。")

    st.markdown(
        '<div class="step-heading"><span class="step-kicker">第二步</span>选择选题并生成脚本</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.topics:
        st.info("先在第一步生成选题，再选择一个方向继续生成脚本。")
    else:
        topic_columns = st.columns(3)
        for index, topic in enumerate(st.session_state.topics):
            with topic_columns[index % 3]:
                with st.container(border=True):
                    st.markdown(f"#### {topic['title']}")
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

        selected_topic = st.session_state.selected_topic
        if selected_topic:
            st.markdown("##### 已选选题")
            st.info(f"{selected_topic['title']}：{selected_topic['summary']}")

        if st.button(
            "生成三段式脚本",
            use_container_width=True,
            disabled=not bool(selected_topic),
        ):
            st.session_state.script = generate_script(st.session_state.selected_topic)
            st.session_state.storyboard = None
            st.success("脚本已生成。")

    if st.session_state.script:
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

    st.markdown(
        '<div class="step-heading"><span class="step-kicker">第三步</span>生成分镜并导出方案</div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown('<div class="section-note">将三段式脚本拆成可执行的镜头表，并保存到历史记录。</div>', unsafe_allow_html=True)
        if st.button(
            "生成分镜并保存历史",
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
        st.markdown("##### 分镜表")
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

with right:
    with st.container(border=True):
        st.markdown("#### 项目状态")
        st.write("当前模式：Mock 数据")
        st.write("可扩展方向：Claude、OpenAI、DeepSeek 等真实大模型 API")

    with st.container(border=True):
        st.markdown("#### 项目价值说明")
        st.write("- 解决短剧/短视频生产中的重复整理问题")
        st.write("- 将业务流程拆解为工具流程")
        st.write("- 支持结构化输出，方便团队复用")
        st.write("- 后续可接入 Claude、OpenAI、DeepSeek 等大模型 API")

    st.markdown("#### 历史记录")
    history = load_history()

    if not history:
        st.info("还没有历史记录。生成分镜后会自动保存。")
    else:
        for index, item in enumerate(history[:5]):
            topic = item.get("topic", {})
            with st.expander(topic.get("title", "未命名方案")):
                st.caption(item.get("created_at", ""))
                st.write(topic.get("summary", ""))
                if st.button("恢复这个方案", key=f"restore_{index}_{item.get('created_at', '')}"):
                    st.session_state.topics = [topic] if topic else []
                    st.session_state.selected_topic_index = 0 if topic else None
                    st.session_state.selected_topic = topic
                    st.session_state.script = item.get("script")
                    st.session_state.storyboard = item.get("storyboard")
                    st.rerun()
