# 项目设计说明

## 主题

请说明你选择的题目和目标用户。

## 数据模型

请说明主要数据字段，例如：标题、分类、日期、状态、备注等。

## 模块分工

- `models.py`：数据模型
- `storage.py`：JSON 读写
- `services.py`：业务逻辑
- `analysis.py`：统计分析
- `cli.py`：命令行入口
- `app.py`：Streamlit 页面入口

## CLI 与 Streamlit 如何共用逻辑

请说明两个入口如何调用同一套 service/storage/analysis 代码。
