# Python 程序设计大作业模板

本模板用于 Python 程序设计期末大作业。你需要完成一个**同时支持 CLI 和 Streamlit 页面操作的个人数据应用**。

核心要求：

- 必须保留 CLI 命令行入口。
- 必须提供 Streamlit 页面入口。
- 禁止使用 Tkinter 作为最终交付。
- 禁止使用 Notebook 作为最终交付。
- CLI 和 Streamlit 必须共用同一套业务逻辑，不能写两套重复代码。
- 数据保存在本地 JSON 文件中。
- 最终提交 commit message 必须包含 `提交作业`。

## 从模板创建自己的仓库

请先用本模板创建你自己的作业仓库，再在自己的仓库中完成开发和提交。

仓库拥有者和命名方式：

- 拥有者（Owner）请选择当前课程组织：`python-final-project-2026-xinguan`
- 仓库名（Repository name）不能使用中文，统一使用小写英文、数字和连字符

推荐仓库名：

```text
python-final-project-<student-id>
```

例如：

```text
python-final-project-2026-xinguan123456
```

创建步骤：

1. 打开本模板仓库页面。
2. 点击页面上的 `Use this template` / `使用此模板`。
3. 拥有者 / Owner 选择：`python-final-project-2026-xinguan`。
4. 仓库名称 / Repository name 填写：`python-final-project-<student-id>`，不要使用中文。
5. 克隆你自己的仓库到本地。
6. 在自己的仓库中完成代码、文档、截图和测试。
7. 最终提交时，commit message 必须包含 `提交作业`。

请不要直接在模板仓库中提交作业。

## 你要完成什么

你需要从 `ASSIGNMENT_TOPICS.md` 中选择一个主题，完成一个个人数据应用。应用至少包含：

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

本模板自带一个“学习记录管理器”示例，用来演示推荐结构。你可以参考它，但最终项目必须改造成你选择的题目。

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

## 最终报告

当你的最终提交 commit message 包含 `提交作业` 时，Gitea Actions 会自动生成：

```text
dist/final-project-report.docx
```

你可以在仓库页面的 `Actions` 对应运行中下载 artifact：`final-project-report`。

报告内容来自：

- `docs/STUDENT_INFO.yml`
- `docs/DESIGN.md`
- `docs/USAGE_EXAMPLES.md`
- `docs/AI_REFLECTION.md`
- `docs/SCREENSHOTS.md`
- `docs/screenshots/`
- 当前仓库提交信息

## 提交前自查

- [ ] 仓库名不是中文。
- [ ] Owner 是 `python-final-project-2026-xinguan`。
- [ ] CLI 可以运行。
- [ ] Streamlit 页面可以运行。
- [ ] 数据能保存到 JSON，重启后仍存在。
- [ ] `pytest -q` 通过。
- [ ] `docs/STUDENT_INFO.yml` 已填写。
- [ ] `docs/USAGE_EXAMPLES.md` 已填写。
- [ ] `docs/AI_REFLECTION.md` 已填写。
- [ ] 最终提交 commit message 包含 `提交作业`。
