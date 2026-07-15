# Python 项目结构知识

> 你看到的大部分 Python 项目都有相似的结构。本文带你一次搞懂每一层是干什么的。

---

## 1. 一图总览

```
my_project/
│
├── src/                          ← 源代码（核心逻辑）
│   └── my_package/               ← 你的 Python 包名
│       ├── __init__.py           ← 把这个文件夹变成"包"
│       ├── models.py             ← 数据模型（dataclass/类）
│       ├── storage.py            ← 数据读写（JSON/数据库）
│       ├── services.py           ← 业务逻辑（增删改查）
│       ├── analysis.py           ← 统计分析
│       └── validators.py         ← 输入校验
│
├── app.py                        ← 应用入口（放在根目录）
├── cli.py                        ← 命令行入口（或 cli/ 文件夹）
│
├── tests/                        ← 测试代码（独立于源码）
│   ├── test_models.py
│   └── test_services.py
│
├── data/                         ← 运行时数据文件
├── docs/                         ← 文档
│
├── pyproject.toml                ← 项目配置与依赖管理
├── requirements.txt              ← 依赖清单（快速安装用）
├── README.md                     ← 项目说明
└── .gitignore                    ← Git 忽略规则
---

## 2. `src/` 目录 — 为什么存在

### 解决的问题

没有 `src/` 时，你的包直接放在根目录：

```
# ❌ 不好的结构
my_project/
  models.py       ← 和 README、配置文件混在一起
  cli.py
```

这样会**引起导入混乱**。Python 运行时会把当前目录加到搜索路径，你可能在不知情下导入到错误的东西。

有了 `src/`：

```
# ✅ 好的结构
src/
  my_package/
    models.py
cli.py → from my_package.models import ...
```

配合 `pyproject.toml` 中的：

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

项目会被安装成包（`pip install -e .`），Python 在任何地方都能正确找到 `from my_package import xxx`。

### 一句话

> **`src/` 让你的代码像第三方库一样"干净地"被导入。**

---

## 3. `my_package/` — 你的包名

`src` 里面这层是**你的 Python 包名**。

- 必须包含 `__init__.py`（可以是空文件）——告诉 Python"这是一个包"
- 通过 `from 包名.模块名 import xxx` 来引用
- 包名通常用**小写字母 + 下划线**，例如 `final_project`、`my_utils`、`data_processor`

包内拆分成多个 `.py` 文件是为了**分层**：

```
入口层（cli.py / app.py）
      ↓
业务逻辑层（services.py）
      ↓
数据层（models.py + storage.py + analysis.py + validators.py）
```

**每一层只关心自己的事，修改一个不影响其他。**

---

## 4. `__init__.py` — 让你把文件夹变成包

当你写 `from my_package.models import xxx` 时，Python 需要知道 `my_package` 是一个"包"而不是普通文件夹。`__init__.py` 就是这个标记。

```python
# src/my_package/__init__.py
"""这是项目描述"""
__version__ = "0.1.0"
```

也可以在 `__init__.py` 里控制"别人导入这个包时，能直接拿到什么"：

```python
# 用户在 from my_package import xxx 时可以用
# 简化对外接口

from .models import MyModel
from .services import MyService

__all__ = ["MyModel", "MyService"]
```

---

## 5. 根目录的文件们

### `app.py` — 为什么放在根目录？

`app.py` 是你的**应用启动入口**。

为什么不在 `src` 里面？因为很多工具（Streamlit、Flask、FastAPI）默认从当前目录找启动文件：

```bash
# 如果 app.py 在根目录
streamlit run app.py

# 如果 app.py 在 src 里面，每次都要写完整路径
streamlit run src/my_package/app.py
```

所以**入口文件放根目录，业务逻辑放 `src`**，这是行业惯例。

### `tests/` — 为什么放在外面？

测试是**验证你的代码的代码**，不是业务逻辑本身，所以和源码分开。

pytest 会自动发现 `tests/` 目录，按名字匹配 `test_*.py` 文件。

```
tests/
  test_models.py      ← 测试数据模型
  test_storage.py     ← 测试数据读写
  test_services.py    ← 测试业务逻辑
  test_cli.py         ← 测试命令行
```

### `pyproject.toml` vs `requirements.txt`

| 文件 | 作用 | 典型内容 | 使用命令 |
|------|------|---------|---------|
| `pyproject.toml` | 项目元信息、依赖、构建配置 | 项目名、版本、Python 版本、依赖 | `pip install -e .` |
| `requirements.txt` | 依赖清单（快速安装） | `streamlit>=1.35` `pytest>=8` | `pip install -r requirements.txt` |

- `pyproject.toml` 是**给 Python 工具链看的**（setuptools、pip、pytest、mypy 等）
- `requirements.txt` 是**给人看的**——别人快速知道要装哪些包

---

## 6. 其他常见文件和目录

### `data/`

运行时生成的数据文件（JSON、CSV、SQLite 等）。通常会被 `.gitignore` 排除（不提交到 Git），只保留一个示例数据文件。

### `docs/`

所有文档：设计说明、使用示例、截图、报告材料。

### `.gitignore`

告诉 Git 哪些文件不需要追踪：

```
__pycache__/     ← Python 缓存文件
.venv/           ← 虚拟环境
*.pyc            ← 编译后的字节码
data/*.json      ← 运行产生的数据（但保留示例数据）
dist/            ← 构建产物
```

---

## 7. 不同项目规模的常见结构

### 第 1 阶段：单文件脚本（< 100 行）

```
my_script.py
data.json
```

### 第 2 阶段：多文件脚本（100-500 行）

```
my_project/
  main.py
  utils.py
  data.json
```

### 第 3 阶段：结构化项目（本课程的标准）

```
my_project/
  src/
    my_package/
      __init__.py
      models.py
      storage.py
      services.py
      analysis.py
  app.py
  tests/
  docs/
  pyproject.toml
```

### 第 4 阶段：可发布的开源库

```
package-name/
  src/package_name/
    __init__.py
    core.py
    utils.py
  tests/
    test_core.py
  docs/
  examples/
  scripts/
  pyproject.toml
  README.md
  LICENSE
  CHANGELOG.md
```

---

## 8. 一句话核心原则

> **入口文件放根目录，业务逻辑放 `src` 里分层放，测试放 `tests` 里。**

你现在写的这个项目（CLI + Streamlit + 分层架构）就是第 3 阶段的标准结构。把这次的结构搞清楚，以后看任何 Python 项目都不会晕了。

---

## 9. 快速自查清单

- [ ] `src/` 里放核心代码（不是入口文件）
- [ ] 你的包名是**小写 + 下划线**
- [ ] 每个包目录都有 `__init__.py`
- [ ] 入口文件（`app.py` / `cli.py`）在根目录
- [ ] 测试文件在 `tests/` 目录，以 `test_` 开头
- [ ] `.gitignore` 排除了缓存和运行时数据
- [ ] `pyproject.toml` 配置了包查找路径 `where = ["src"]`