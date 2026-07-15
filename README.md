# Python 程序设计大作业模板

本项目改编自作者2026年6月大一下学期 Python 程序设计期末大作业。我需要完成一个**同时支持 CLI 和 Streamlit 页面操作的个人数据应用**。

我的选题是：**AI 学习复盘记录系统** 

记录学习问题、AI 回答摘要、自己的理解、复盘标签，支持搜索和复盘统计。

核心要求：

- 必须保留 CLI 命令行入口。
- 必须提供 Streamlit 页面入口。
- 禁止使用 Tkinter 作为最终交付。
- 禁止使用 Notebook 作为最终交付。
- CLI 和 Streamlit 必须共用同一套业务逻辑，不能写两套重复代码。
- 数据保存在本地 JSON 文件中。
- 最终提交 commit message 必须包含 `提交作业`。


## 我完成了什么

选择一个主题，完成一个个人数据应用。应用至少包含：

- 数据录入
- 数据查看
- 数据搜索或过滤
- 数据更新或删除
- 统计分析
- JSON 保存和读取
- CLI 操作
- Streamlit 页面操作
- pytest 测试
- README 和最终报告材料

## 安装和运行

建议使用虚拟环境：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

### 运行 CLI

```bash
python -m final_project.cli --help
python -m final_project.cli add "完成 Week 10 作业" --category 学习 --duration 90 --note "复习 JSON"
python -m final_project.cli list
python -m final_project.cli search JSON
python -m final_project.cli stats
```

### 运行 Streamlit 页面

```bash
streamlit run app.py
```

### 运行测试

```bash
pytest -q
```

## 推荐项目结构

```text
src/final_project/
  cli.py          # CLI 入口，只负责命令行参数和输出
  models.py       # dataclass 数据模型
  storage.py      # JSON 文件读写
  services.py     # 增删改查业务逻辑
  analysis.py     # 统计分析
  validators.py   # 输入校验
app.py            # Streamlit 入口，只负责页面展示和交互
tests/            # pytest 测试
docs/             # 学生信息、使用示例、AI 反思、截图说明
report/           # Word 报告生成脚本
```

关键原则：

```text
CLI / Streamlit
      ↓
services.py
      ↓
models.py + storage.py + analysis.py
```

不要把主要业务逻辑直接写在 `cli.py` 或 `app.py` 中。

