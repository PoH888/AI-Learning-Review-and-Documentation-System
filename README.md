# Python Programming Final Project

This project is adapted from the author's Python Programming final project at the end of the first year (June 2026). I need to build a **personal data application that supports both CLI and Streamlit web interface**.

My chosen topic is: **AI Learning Review & Documentation System**

Record learning questions, AI answer summaries, your own understanding, and review tags, with search and review statistics.

Core requirements:

- CLI entry point must be preserved.
- Streamlit page entry must be provided.
- Tkinter is not allowed in the final submission.
- Notebook is not allowed in the final submission.
- CLI and Streamlit must share the same business logic — no duplicate code.
- Data is stored in local JSON files.
- The final commit message must contain `提交作业`.

## What I've Completed

Choose a topic and build a personal data application. The application must include:

- Data entry
- Data viewing
- Data search or filtering
- Data update or deletion
- Statistical analysis
- JSON save and load
- CLI operations
- Streamlit page operations
- pytest tests
- README and final report materials

## Installation and Usage

It is recommended to use a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

### Running the CLI

```bash
python -m final_project.cli --help
python -m final_project.cli add "What is a decorator" --ai-summary "A form of AOP programming" --tags "Python,Advanced"
python -m final_project.cli list
python -m final_project.cli search decorator
python -m final_project.cli stats
```

### Running the Streamlit App

```bash
streamlit run app.py
```

### Running Tests

```bash
pytest -q
```

## Recommended Project Structure

```text
src/final_project/
  cli.py          # CLI entry point: handles command-line arguments and output only
  models.py       # Dataclass data model
  storage.py      # JSON file read/write
  services.py     # CRUD business logic
  analysis.py     # Statistical analysis
  validators.py   # Input validation
app.py            # Streamlit entry point: handles page display and interaction only
tests/            # pytest tests
docs/             # Student info, usage examples, AI reflections, screenshots
report/           # Word report generation script
```

Key design principle:

```text
CLI / Streamlit
      ↓
services.py
      ↓
models.py + storage.py + analysis.py
```

Do not put core business logic directly in `cli.py` or `app.py`.
