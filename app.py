from pathlib import Path

import streamlit as st

from final_project.services import ReviewService
from final_project.storage import StorageError

service = ReviewService()

st.set_page_config(page_title="AI 学习复盘记录系统", page_icon="🤖")
st.title("🤖 AI 学习复盘记录系统")
st.caption("记录你向 AI 提的问题、回答摘要和自己的理解，支持搜索和复盘统计。")

with st.form("add-review"):
    question = st.text_input("你的问题 *", placeholder="例如：什么是 Python 装饰器？")
    ai_summary = st.text_area("AI 回答摘要", placeholder="记录 AI 给出的关键点")
    understanding = st.text_area("自己的理解", placeholder="你学到了什么？")
    tags_input = st.text_input("标签（逗号分隔）", placeholder="Python,进阶")
    submitted = st.form_submit_button("添加复盘")
    if submitted:
        try:
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            review = service.add_review(question, ai_summary, understanding, tags)
            st.success(f"已添加复盘 #{review.id}")
            st.rerun()
        except (ValueError, StorageError) as exc:
            st.error(str(exc))

try:
    reviews = service.list_reviews()
    stats = service.stats()
except StorageError as exc:
    st.error(str(exc))
    reviews = []
    stats = {"count": 0, "count_by_tag": {}, "count_by_date": {}}

col1, col2 = st.columns(2)
col1.metric("复盘总数", stats["count"])
col2.metric("累计标签数", len(stats.get("count_by_tag", {})))

keyword = st.text_input("搜索关键词")
shown = service.search_reviews(keyword) if keyword.strip() else reviews

st.subheader("复盘列表")
if not shown:
    st.info("暂无复盘记录。")
else:
    for review in shown:
        tags_str = "，".join(review.tags) if review.tags else "无标签"
        with st.expander(f"#{review.id} {review.question} [{tags_str}]"):
            st.write(f"**AI 回答摘要：** {review.ai_summary or '（无）'}")
            st.write(f"**自己的理解：** {review.understanding or '（无）'}")
            st.write(f"**日期：** {review.created_at}")

            with st.form(f"edit-review-{review.id}"):
                new_question = st.text_input("问题", value=review.question)
                new_ai_summary = st.text_area("AI 回答摘要", value=review.ai_summary)
                new_understanding = st.text_area("自己的理解", value=review.understanding)
                new_tags = st.text_input("标签（逗号分隔）", value="，".join(review.tags))
                if st.form_submit_button("保存修改"):
                    try:
                        tags = [t.strip() for t in new_tags.split("，") if t.strip()]
                        service.update_review(
                            review.id,
                            question=new_question,
                            ai_summary=new_ai_summary,
                            understanding=new_understanding,
                            tags=tags,
                        )
                        st.success("已修改")
                        st.rerun()
                    except (ValueError, StorageError) as exc:
                        st.error(str(exc))

st.subheader("标签统计")
if stats["count_by_tag"]:
    st.bar_chart(stats["count_by_tag"])
else:
    st.info("还没有可统计的数据。")
