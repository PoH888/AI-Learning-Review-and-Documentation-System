from __future__ import annotations

import argparse
from pathlib import Path

from .services import RecordService
from .storage import DEFAULT_DATA_PATH, StorageError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python 大作业示例：学习记录管理器")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH, help="JSON 数据文件路径")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="添加记录")
    add.add_argument("title")
    add.add_argument("--category", default="未分类")
    add.add_argument("--duration", type=int, default=0)
    add.add_argument("--note", default="")

    subparsers.add_parser("list", help="列出记录")

    search = subparsers.add_parser("search", help="搜索记录")
    search.add_argument("keyword")

    delete = subparsers.add_parser("delete", help="删除记录")
    delete.add_argument("id", type=int)

    subparsers.add_parser("stats", help="查看统计")
    return parser


def format_record(record) -> str:
    return f"#{record.id} [{record.category}] {record.title} - {record.duration_minutes}分钟 ({record.created_at})"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    service = RecordService(args.data)

    try:
        if args.command == "add":
            record = service.add_record(args.title, args.category, args.duration, args.note)
            print(f"已添加：{format_record(record)}")
        elif args.command == "list":
            records = service.list_records()
            if not records:
                print("暂无记录")
            for record in records:
                print(format_record(record))
        elif args.command == "search":
            records = service.search_records(args.keyword)
            if not records:
                print("没有找到匹配记录")
            for record in records:
                print(format_record(record))
        elif args.command == "delete":
            if service.delete_record(args.id):
                print(f"已删除记录 #{args.id}")
            else:
                print(f"未找到记录 #{args.id}")
                return 1
        elif args.command == "stats":
            stats = service.stats()
            print(f"记录数量：{stats['count']}")
            print(f"总时长：{stats['total_duration']} 分钟")
            print(f"分类统计：{stats['count_by_category']}")
        return 0
    except (ValueError, StorageError) as exc:
        print(f"错误：{exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
