import streamlit as st

from services.topic_service import generate_topics
from services.script_service import generate_script
from services.storyboard_service import generate_storyboard
from utils.storage import save_record, load_history, build_markdown


st.set_page_config(
    page_title="AI短剧/短视频生产效率工具",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }
    .main-title { font-size: 34px; font-weight: 800; margin-bottom: 4px; }
    .sub-title { color: #666; font-size: 15px; margin-bottom: 22px; }
    .tag { display: inline-block; padding: 4px 10px; border: 1px solid #ddd; border-radius: 20px; margin-right: 8px; color: #444; font-size: 13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">AI短剧/短视频生产效率工具</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">输入主题 → 生成选题 → 生成脚本 → 拆解分镜 → 导出方案。当前版本使用 Mock 数据，适合演示 AI 工具开发流程。</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<span class="tag">AI辅助开发</span><span class="tag">短剧/短视频</span><span class="tag">效率工具</span><span class="tag">Prompt模板</span><span class="tag">可演示MVP</span>',
    unsafe_allow_html=True,
)

if "topics" not in st.session_state:
    st.session_state.topics = []
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None
if "script" not in st.session_state:
    st.session_state.script = None
if "storyboard" not in st.session_state:
    st.session_state.storyboard = None

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("1. 输入内容主题")
    theme = st.text_input(
        "主题",
        placeholder="例如：末日求生、山海经怪谈、未来科幻、都市反转",
    )

    if st.button("生成选题", type="primary", use_container_width=True):
        st.session_state.topics = generate_topics(theme)
        st.session_state.selected_topic = None
        st.session_state.script = None
        st.session_state.storyboard = None
        st.success("已生成 3 个选题。")

    if st.session_state.topics:
        st.subheader("2. 选择一个选题")
        titles = [item["title"] for item in st.session_state.topics]
        selected_title = st.radio("选题列表", titles)

        selected_topic = next(item for item in st.session_state.topics if item["title"] == selected_title)
        st.session_state.selected_topic = selected_topic

        with st.container(border=True):
            st.markdown(f"### {selected_topic['title']}")
            st.write(selected_topic["summary"])
            st.write(f"**爆点：** {selected_topic['hook']}")
            st.write(f"**适合平台：** {selected_topic['platform']}")

        if st.button("生成脚本", use_container_width=True):
            st.session_state.script = generate_script(st.session_state.selected_topic)
            st.session_state.storyboard = None
            st.success("脚本已生成。")

    if st.session_state.script:
        st.subheader("3. 三段式脚本")
        script = st.session_state.script
        st.markdown("**开场**")
        st.write(script["opening"])
        st.markdown("**冲突**")
        st.write(script["conflict"])
        st.markdown("**结尾**")
        st.write(script["ending"])

        if st.button("生成分镜表", use_container_width=True):
            st.session_state.storyboard = generate_storyboard(st.session_state.script)
            record = {
                "theme": theme,
                "topic": st.session_state.selected_topic,
                "script": st.session_state.script,
                "storyboard": st.session_state.storyboard,
            }
            save_record(record)
            st.success("分镜表已生成，并保存到历史记录。")

    if st.session_state.storyboard:
        st.subheader("4. 分镜表")
        st.dataframe(st.session_state.storyboard, use_container_width=True, hide_index=True)

        record = {
            "theme": theme,
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
    st.subheader("历史记录")
    history = load_history()

    if not history:
        st.info("还没有历史记录。生成分镜后会自动保存。")
    else:
        for item in history[:5]:
            topic = item.get("topic", {})
            with st.expander(topic.get("title", "未命名方案")):
                st.caption(item.get("created_at", ""))
                st.write(topic.get("summary", ""))
                if st.button("恢复这个方案", key=item.get("created_at", "")):
                    st.session_state.selected_topic = item.get("topic")
                    st.session_state.script = item.get("script")
                    st.session_state.storyboard = item.get("storyboard")
                    st.rerun()

    st.divider()
    st.subheader("项目说明")
    st.write(
        "这个项目用于展示：如何把短剧/短视频生产流程拆成可复用工具，并通过 AI 辅助开发提升效率。"
    )
    st.write("后续可以接入真实大模型 API，替换当前 Mock 数据。")
