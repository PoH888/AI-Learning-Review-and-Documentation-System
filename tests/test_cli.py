from final_project.cli import main


def test_cli_add_and_list(tmp_path, capsys):
    data = tmp_path / "records.json"
    assert main(["--data", str(data), "add", "测试 CLI", "--category", "学习", "--duration", "15"]) == 0
    assert main(["--data", str(data), "list"]) == 0
    out = capsys.readouterr().out
    assert "测试 CLI" in out
