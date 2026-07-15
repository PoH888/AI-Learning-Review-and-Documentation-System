from final_project.cli import main


def test_cli_add_and_list(tmp_path, capsys):
    data = tmp_path / "reviews.json"
    assert main(["--data", str(data), "add", "什么是装饰器", "--tags", "Python,进阶"]) == 0
    assert main(["--data", str(data), "list"]) == 0
    out = capsys.readouterr().out
    assert "装饰器" in out