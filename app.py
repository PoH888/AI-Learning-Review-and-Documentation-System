from pathlib import Path

import streamlit as st

from final_project.services import RecordService
from final_project.storage import StorageError

DATA_PATH = Path("data/records.json")
service = RecordService(DATA_PATH)

st.set_page_config(page_title="Python 大作业示例", page_icon="🐍")
st.title("🐍 Python 大作业示例：学习记录管理器")
st.caption("请把这个示例改造成你自己选择的题目。CLI 和 Streamlit 应共用 services/storage/analysis 逻辑。")

with st.form("add-record"):
    title = st.text_input("标题")
    category = st.text_input("分类", value="学习")
    duration = st.number_input("时长（分钟）", min_value=0, step=5)
    note = st.text_area("备注")
    submitted = st.form_submit_button("添加记录")
    if submitted:
        try:
            record = service.add_record(title, category, int(duration), note)
            st.success(f"已添加记录 #{record.id}")
        except (ValueError, StorageError) as exc:
            st.error(str(exc))

try:
    records = service.list_records()
    stats = service.stats()
except StorageError as exc:
    st.error(str(exc))
    records = []
    stats = {"count": 0, "total_duration": 0, "duration_by_category": {}}

col1, col2 = st.columns(2)
col1.metric("记录数量", stats["count"])
col2.metric("总时长（分钟）", stats["total_duration"])

keyword = st.text_input("搜索关键词")
shown = service.search_records(keyword) if keyword.strip() else records

st.subheader("记录列表")
if shown:
    st.table([record.to_dict() for record in shown])
else:
    st.info("暂无记录。")

st.subheader("按分类统计时长")
duration_by_category = stats.get("duration_by_category", {})
if duration_by_category:
    st.bar_chart(duration_by_category)
else:
    st.info("还没有可统计的数据。")
